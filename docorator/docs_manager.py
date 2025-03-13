from typing import Dict, Any, Optional, List, Union, Tuple
import io
import re
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from docx import Document
from docx.document import Document as DocxDocument
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.table import Table, _Cell
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from logorator import Logger
from .auth import GoogleAuth
from .exceptions import DocumentNotFoundError, DocumentCreationError, DocumentSaveError


class Docorator:
    def __init__(self, keyfile_path: str, email: Optional[str] = None) -> None:
        self.auth = GoogleAuth(keyfile_path)
        self.docs_service = self.auth.get_docs_service()
        self.drive_service = self.auth.get_drive_service()
        self.email = email

    @Logger()
    def _find_document_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.document'"
        results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            return None

        return files[0]

    @Logger()
    def _create_document(self, name: str) -> Dict[str, Any]:
        try:
            file_metadata = {
                'name'    : name,
                'mimeType': 'application/vnd.google-apps.document'
            }
            document = self.drive_service.files().create(body=file_metadata).execute()

            # Set document to be editable by anyone
            anyone_permission = {
                'type': 'anyone',
                'role': 'writer'
            }
            self.drive_service.permissions().create(
                fileId=document['id'],
                body=anyone_permission
            ).execute()

            # Add email-specific sharing
            if self.email:
                try:
                    email_permission = {
                        'type'        : 'user',
                        'role'        : 'writer',
                        'emailAddress': self.email
                    }
                    self.drive_service.permissions().create(
                        fileId=document['id'],
                        body=email_permission,
                        sendNotificationEmail=False,
                        fields='id'
                    ).execute()
                except Exception as e:
                    # Log the error but continue with the document creation
                    Logger.note(f"Warning: Failed to share document with {self.email}: {str(e)}")

            return document
        except Exception as e:
            raise DocumentCreationError(f"Failed to create document: {str(e)}")

    @Logger()
    def _export_to_docx(self, document_id: str) -> DocxDocument:
        try:
            request = self.drive_service.files().export_media(
                fileId=document_id,
                mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            file.seek(0)
            return Document(file)
        except Exception as e:
            raise DocumentNotFoundError(f"Failed to export document to DOCX: {str(e)}")

    @Logger()
    def _upload_docx_as_google_doc(self, name: str, docx_document: DocxDocument) -> Dict[str, Any]:
        try:
            file_buffer = io.BytesIO()
            docx_document.save(file_buffer)
            file_buffer.seek(0)

            file_metadata = {
                'name'    : name,
                'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }

            media = MediaIoBaseUpload(
                file_buffer,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                resumable=True
            )

            uploaded_file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()

            converted_metadata = {
                'mimeType': 'application/vnd.google-apps.document'
            }

            converted_file = self.drive_service.files().update(
                fileId=uploaded_file['id'],
                body=converted_metadata
            ).execute()

            # Set document to be editable by anyone
            anyone_permission = {
                'type': 'anyone',
                'role': 'writer'
            }
            self.drive_service.permissions().create(
                fileId=converted_file['id'],
                body=anyone_permission
            ).execute()

            # Share with specific email if provided
            if self.email:
                email_permission = {
                    'type'        : 'user',
                    'role'        : 'writer',
                    'emailAddress': self.email
                }
                self.drive_service.permissions().create(
                    fileId=converted_file['id'],
                    body=email_permission,
                    sendNotificationEmail=True
                ).execute()

            return converted_file
        except Exception as e:
            raise DocumentSaveError(f"Failed to upload DOCX as Google Doc: {str(e)}")

    @Logger()
    def get_document(self, name: str) -> DocxDocument:
        document = self._find_document_by_name(name)

        if not document:
            document = self._create_document(name)

        return self._export_to_docx(document['id'])

    @Logger()
    def save_document(self, name: str, docx_document: DocxDocument) -> bool:
        try:
            existing_document = self._find_document_by_name(name)

            if existing_document:
                # If document exists, update its content directly
                file_buffer = io.BytesIO()
                docx_document.save(file_buffer)
                file_buffer.seek(0)

                media = MediaIoBaseUpload(
                    file_buffer,
                    mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    resumable=True
                )

                updated_file = self.drive_service.files().update(
                    fileId=existing_document['id'],
                    media_body=media
                ).execute()

                return True
            else:
                # If document doesn't exist, create a new one
                file_metadata = {
                    'name'    : name,
                    'mimeType': 'application/vnd.google-apps.document'
                }

                file_buffer = io.BytesIO()
                docx_document.save(file_buffer)
                file_buffer.seek(0)

                media = MediaIoBaseUpload(
                    file_buffer,
                    mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    resumable=True
                )

                new_file = self.drive_service.files().create(
                    body=file_metadata,
                    media_body=media
                ).execute()

                # Convert to Google Docs format
                converted_metadata = {
                    'mimeType': 'application/vnd.google-apps.document'
                }

                converted_file = self.drive_service.files().update(
                    fileId=new_file['id'],
                    body=converted_metadata
                ).execute()

                # Set document to be editable by anyone
                anyone_permission = {
                    'type': 'anyone',
                    'role': 'writer'
                }
                self.drive_service.permissions().create(
                    fileId=converted_file['id'],
                    body=anyone_permission
                ).execute()

                # Share with specific email if provided
                if self.email:
                    email_permission = {
                        'type'        : 'user',
                        'role'        : 'writer',
                        'emailAddress': self.email
                    }
                    self.drive_service.permissions().create(
                        fileId=converted_file['id'],
                        body=email_permission,
                        sendNotificationEmail=True
                    ).execute()

                return True

        except Exception as e:
            raise DocumentSaveError(f"Failed to save document: {str(e)}")

    @Logger()
    def convert_docx_to_markdown(self, docx_document: DocxDocument) -> str:
        md_lines = []

        for element in docx_document.element.body:
            if isinstance(element, CT_P):
                paragraph = Paragraph(element, docx_document)
                md_lines.append(self._convert_paragraph_to_markdown(paragraph))
            elif isinstance(element, CT_Tbl):
                table = Table(element, docx_document)
                md_lines.append(self._convert_table_to_markdown(table))

        return "\n\n".join(line for line in md_lines if line)

    @Logger()
    def _convert_paragraph_to_markdown(self, paragraph: Paragraph) -> str:
        # Check if this is a heading
        if paragraph.style.name.startswith('Heading'):
            level = int(paragraph.style.name[-1])
            return '#' * level + ' ' + self._convert_runs_to_markdown(paragraph.runs)

        # Check if this is a list
        if paragraph.style.name.startswith('List'):
            text = self._convert_runs_to_markdown(paragraph.runs)
            # Handle numbered vs bullet list
            if 'Number' in paragraph.style.name:
                return f"1. {text}"
            else:
                return f"- {text}"

        # Regular paragraph
        return self._convert_runs_to_markdown(paragraph.runs)

    @Logger()
    def _convert_runs_to_markdown(self, runs: List[Run]) -> str:
        result = []
        for run in runs:
            text = run.text

            # Apply formatting
            if run.bold:
                text = f"**{text}**"
            if run.italic:
                text = f"*{text}*"
            if run.underline:
                text = f"__{text}__"

            result.append(text)

        return "".join(result)

    @Logger()
    def _convert_table_to_markdown(self, table: Table) -> str:
        if not table.rows:
            return ""

        md_lines = []

        # Process header row
        header_cells = []
        for cell in table.rows[0].cells:
            cell_text = self._extract_cell_text(cell)
            header_cells.append(cell_text)

        md_lines.append("| " + " | ".join(header_cells) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(header_cells)) + " |")

        # Process data rows
        for row in table.rows[1:]:
            row_cells = []
            for cell in row.cells:
                cell_text = self._extract_cell_text(cell)
                row_cells.append(cell_text)
            md_lines.append("| " + " | ".join(row_cells) + " |")

        return "\n".join(md_lines)

    @Logger()
    def _extract_cell_text(self, cell: _Cell) -> str:
        text_parts = []
        for paragraph in cell.paragraphs:
            text_parts.append(self._convert_runs_to_markdown(paragraph.runs))

        # Replace pipe characters which would break markdown tables
        cell_text = " ".join(text_parts)
        cell_text = cell_text.replace("|", "\\|")

        return cell_text