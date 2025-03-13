# Docorator

Docorator is a Python library for seamless Google Docs integration with persistent caching capabilities. It enables programmatic creation, editing, and management of Google Docs with Markdown support.

## Features

- Create and manage Google Docs through an intuitive Python interface
- Convert between Google Docs and Markdown formats
- Automatic document sharing and permission management
- Threaded operations for non-blocking performance
- Persistent caching via [Cacherator](https://github.com/Redundando/cacherator)
- Detailed operation logging with [Logorator](https://github.com/Redundando/logorator)
- Support for converting between Markdown, HTML, and DOCX formats

## Installation

```bash
pip install docorator
```

## Requirements

- Python 3.7+
- Google API service account credentials

## Quick Start

```python
from docorator import Docorator

# Initialize with your service account key file
doco = Docorator(
    keyfile_path="service-account-key.json",
    email="your-email@example.com",  # Optional email to share the document with
    document_name="My Document"
)

# Wait for the document to load (creates a new document if it doesn't exist)
doco.wait_for_load()

# Get document content as Markdown
markdown_content = doco.as_markdown()
print(markdown_content)

# Update the document with new Markdown content
doco.save("# This is a headline\n\n## Section\n\nHello world!")

# Access the document URL
print(f"Document URL: {doco.url}")
```

## Detailed Usage

### Document Management

```python
# Create or load a document
doco = Docorator(keyfile_path="key.json", email="user@example.com", document_name="My Document")

# Check if document exists (URL is None if document doesn't exist yet)
url = doco.url

# Force reload of document content
doco.load()

# Wait for background loading to complete
doc = doco.wait_for_load()  # Returns a python-docx Document object

# Get Markdown representation
md_content = doco.as_markdown()

# Save Markdown content
doco.save("# New Markdown Content")

# Save a python-docx Document object
from docx import Document
doc = Document()
doc.add_heading("New Document", 0)
doco.save(doc)

# Wait for background save to complete
save_success = doco.wait_for_save()
```

### Asynchronous Operations

Docorator performs document operations in background threads to prevent blocking:

- `load()` initiates document loading in a background thread
- `wait_for_load()` blocks until loading completes
- `save()` initiates document saving in a background thread
- `wait_for_save()` blocks until saving completes

This threading model allows your application to remain responsive while document operations proceed in the background.

### Caching System

Docorator leverages [Cacherator](https://github.com/Redundando/cacherator) for efficient document caching:

- Document IDs, metadata, and state are cached to minimize API calls
- Cache is stored in the `data/docorator` directory by default
- To clear the cache for a document:
  ```python
  doco = Docorator(
      keyfile_path="key.json", 
      email="user@example.com",
      document_name="My Document", 
      clear_cache=True
  )
  ```

## Authentication

Docorator requires a Google service account with access to Google Docs and Drive APIs:

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Google Docs API and Google Drive API
3. Create a service account and download the JSON key file
4. Use the path to this key file in the `keyfile_path` parameter

For more details on setting up Google service accounts, see the [Google Cloud documentation](https://cloud.google.com/iam/docs/creating-managing-service-accounts).

## License

MIT

## Dependencies

- google-auth
- google-api-python-client
- python-docx
- typing-extensions
- google
- logorator
- cacherator
- mammoth
- html2docx
- Markdown