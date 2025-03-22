from typing import Tuple
from io import BytesIO
import re
import markdown
from docx import Document
from htmldocx import HtmlToDocx

def convert_markdown_to_docx(markdown_text: str, title: str = "Document") -> Tuple[BytesIO, int]:
    """
    Converts a Markdown string to a DOCX file in memory using htmldocx.
    Returns a tuple of (BytesIO, file_size_in_bytes).
    """

    # 1) Convert Markdown to HTML
    html_content = markdown.markdown(markdown_text)

    # 2) Optional: Replace <img> tags with alt text
    #    (htmldocx *does* handle images, but if you only want placeholders, do this)
    image_pattern = r'<img[^>]*alt="([^"]*)"[^>]*>'
    html_content = re.sub(image_pattern, lambda m: f'[Image: {m.group(1)}]', html_content)

    # 3) Create a new blank Document
    document = Document()

    # Optionally, set the doc's internal title property
    document.core_properties.title = title

    # 4) Convert the HTML and add it into the Document
    parser = HtmlToDocx()
    parser.add_html_to_document(html_content, document)

    # 5) Write the doc to an in-memory BytesIO buffer
    docx_file = BytesIO()
    document.save(docx_file)

    # Get the file size
    file_size = docx_file.tell()
    docx_file.seek(0)  # Rewind for reading downstream

    return docx_file, file_size
