from typing import Tuple, Optional
from io import BytesIO
import re
import markdown
from html2docx import html2docx


def convert_markdown_to_docx(markdown_text: str, title: str = "Document") -> Tuple[BytesIO, int]:
    html_content = markdown.markdown(markdown_text)

    image_pattern = r'<img[^>]*alt="([^"]*)"[^>]*>'
    html_content = re.sub(image_pattern, lambda m: f'[Image: {m.group(1)}]', html_content)

    # html2docx already returns a BytesIO object
    docx_file = html2docx(html_content, title=title)

    # Get current position
    current_pos = docx_file.tell()

    # Go to end to get size
    docx_file.seek(0, 2)
    file_size = docx_file.tell()

    # Reset position
    docx_file.seek(0)

    return docx_file, file_size