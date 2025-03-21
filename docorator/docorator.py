from typing import Dict, Any, Optional, List, Union
import asyncio
import re
import html2text
from cacherator import JSONCache

from .authentication_helper import AuthenticationHelper
from googleapiclient.http import MediaIoBaseUpload
from logorator import Logger

class Docorator(JSONCache):
    def __init__(self, service_account_file: str, document_id: Optional[str] = None, document_name: Optional[str] = None, email_addresses: Optional[Union[str, List[str]]] = None, clear_cache=False, ttl=7):
        JSONCache.__init__(self, data_id=f"{document_name or document_id or 'default'}", directory="data/docorator", clear_cache=clear_cache, ttl=ttl)
        self.service_account_file = service_account_file
        if not hasattr(self, "document_id"):
            self.document_id = document_id
        self.document_name = document_name
        self.auth_helper = AuthenticationHelper(service_account_file)

        self.email_addresses = []

        if email_addresses:
            if isinstance(email_addresses, str):
                self.email_addresses = [email_addresses]
            else:
                self.email_addresses = email_addresses

    def __str__(self):
        if self.document_name:
            return f"{self.document_name} ({self.url()})"
        return self.url()

    def __repr__(self):
        return self.__str__()

    def url(self):
        if self.document_id:
            return f"https://docs.google.com/document/d/{self.document_id}/edit"
        return None

    @Logger()
    async def initialize(self) -> None:
        await self.auth_helper.authenticate_async()
        if self.document_id is None and self.document_name is not None:
            found_id = await self.find_document_by_name(self.document_name)
            if found_id:
                self.document_id = found_id
                if self.email_addresses:
                    await self.share_document()
                Logger.note(f"Document found ({self.url()})")
            else:
                await self.create_document(self.document_name)

    async def find_document_by_name(self, name: str) -> Optional[str]:
        if not self.auth_helper.drive_service:
            await self.auth_helper.authenticate_async()

        loop = asyncio.get_event_loop()
        query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.document'"
        response = await loop.run_in_executor(None, lambda: self.auth_helper.drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute())

        files = response.get('files', [])
        if files:
            return files[0]['id']
        return None


    @Logger()
    async def create_document(self, name: str) -> str:
        if not self.auth_helper.docs_service:
            await self.auth_helper.authenticate_async()

        loop = asyncio.get_event_loop()
        document_metadata = {'title': name}

        doc = await loop.run_in_executor(None, lambda: self.auth_helper.docs_service.documents().create(body=document_metadata).execute())

        self.document_id = doc['documentId']
        self.document_name = name

        Logger.note(f"Document created ({self.url()})")

        await self.set_anyone_editor()

        if self.email_addresses:
            await self.share_document()

        return self.document_id

    async def set_anyone_editor(self) -> None:
        if not self.document_id or not self.auth_helper.drive_service:
            return

        loop = asyncio.get_event_loop()
        permission = {'type': 'anyone', 'role': 'writer', 'allowFileDiscovery': False}

        await loop.run_in_executor(None, lambda: self.auth_helper.drive_service.permissions().create(fileId=self.document_id, body=permission).execute())

    async def share_document(self) -> None:
        if not self.document_id or not self.auth_helper.drive_service or not self.email_addresses:
            return

        loop = asyncio.get_event_loop()

        for email in self.email_addresses:
            permission = {'type': 'user', 'role': 'writer', 'emailAddress': email}

            await loop.run_in_executor(None, lambda _email=email: self.auth_helper.drive_service.permissions().create(fileId=self.document_id, body=permission, sendNotificationEmail=True).execute())

    async def export_as_html(self) -> Optional[str]:
        if not self.document_id or not self.auth_helper.drive_service:
            return None

        if not self.auth_helper.drive_service:
            await self.auth_helper.authenticate_async()

        loop = asyncio.get_event_loop()

        try:
            response = await loop.run_in_executor(None, lambda: self.auth_helper.drive_service.files().export(fileId=self.document_id, mimeType='text/html').execute())

            if isinstance(response, bytes):
                return response.decode('utf-8')
            return response
        except Exception as e:
            return None

    @Logger()
    async def export_as_markdown(self) -> Optional[str]:
        html_content = await self.export_as_html()
        if not html_content:
            return None

        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0
        h.ignore_images = False
        h.images_to_alt = True

        markdown = h.handle(html_content)
        image_pattern = r'!\[(.*?)\]\(.*?\)'
        markdown = re.sub(image_pattern, lambda m: f'[Image: {m.group(1)}]', markdown)

        return markdown

    @Logger()
    async def update_from_markdown(self, markdown_text: str, title: Optional[str] = None) -> bool:
        from .markdown_converter import convert_markdown_to_docx

        if not self.document_id:
            return False

        if not self.auth_helper.drive_service:
            await self.auth_helper.authenticate_async()

        doc_title = title or self.document_name or "Document"
        docx_file, file_size = convert_markdown_to_docx(markdown_text, title=doc_title)

        media = MediaIoBaseUpload(docx_file, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', resumable=True)

        loop = asyncio.get_event_loop()

        try:
            await loop.run_in_executor(None, lambda: self.auth_helper.drive_service.files().update(fileId=self.document_id, media_body=media, fields='id').execute())
            return True
        except Exception:
            return False