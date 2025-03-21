# Docorator

A Python library for seamless interaction with Google Docs, featuring document creation, editing, and format conversion with built-in caching and logging.

## Features

- Create, find, and share Google Docs
- Convert between Markdown and Google Docs
- Export Google Docs as Markdown or HTML
- Update Google Docs from Markdown content
- Persistent caching for improved performance
- Detailed logging of operations
- Asynchronous API for non-blocking operations

## Installation

```bash
pip install docorator
```

## Dependencies

Docorator depends on the following libraries:
- [Cacherator](https://github.com/Redundando/cacherator): For persistent caching
- [Logorator](https://github.com/Redundando/logorator): For operation logging
- Google API Client libraries
- HTML and Markdown conversion utilities

## Basic Usage

```python
import asyncio
from docorator import Docorator

async def main():
    # Initialize with document name
    doc = Docorator('path/to/service-account-key.json', document_name="My Document")

    # Initialize (creates document if it doesn't exist)
    await doc.initialize()

    # Export document as Markdown
    markdown_content = await doc.export_as_markdown()
    print(markdown_content)

    # Update document with new Markdown content
    new_content = "# Updated Title\nThis is updated content with an ![image](http://example.com/img.jpg)"
    success = await doc.update_from_markdown(new_content)

asyncio.run(main())
```

## API Reference

### Docorator Class

The main class for interacting with Google Docs.

#### Constructor

```python
Docorator(
    service_account_file: str,
    document_id: Optional[str] = None,
    document_name: Optional[str] = None,
    email_addresses: Optional[Union[str, List[str]]] = None,
    clear_cache: bool = False,
    ttl: int = 7
)
```

- **service_account_file**: Path to the Google service account JSON key file
- **document_id**: ID of an existing Google Document (optional)
- **document_name**: Name for the document (used for finding or creating) (optional)
- **email_addresses**: Email addresses to share the document with (optional)
- **clear_cache**: Whether to clear existing cache (default: False)
- **ttl**: Time-to-live for cached data in days (default: 7)

Note: Either `document_id` or `document_name` should be provided.

#### Methods

##### `async initialize() -> None`

Initializes the Docorator instance. If `document_id` is not provided but `document_name` is, this method will:
1. Search for a document with the given name
2. If found, use that document
3. If not found, create a new document with the given name

##### `async find_document_by_name(name: str) -> Optional[str]`

Searches for a Google Document with the specified name.

- **name**: The name of the document to find
- **Returns**: The document ID if found, None otherwise

##### `async create_document(name: str) -> str`

Creates a new Google Document with the specified name.

- **name**: The name for the new document
- **Returns**: The ID of the newly created document

##### `async set_anyone_editor() -> None`

Sets the document's sharing settings to allow anyone with the link to edit.

##### `async share_document() -> None`

Shares the document with the email addresses specified during initialization.

##### `async export_as_html() -> Optional[str]`

Exports the document as HTML.

- **Returns**: The document content as HTML, or None if export fails

##### `async export_as_markdown() -> Optional[str]`

Exports the document as Markdown.

- **Returns**: The document content as Markdown, or None if export fails

##### `async update_from_markdown(markdown_text: str, title: Optional[str] = None) -> bool`

Updates the Google Document with the provided Markdown content.

- **markdown_text**: Markdown content to convert and update the document with
- **title**: New title for the document (optional)
- **Returns**: True if update was successful, False otherwise

##### `url() -> Optional[str]`

Gets the URL of the Google Document.

- **Returns**: The URL of the document, or None if document_id is not set

#### Properties

##### `document_id: str`

The ID of the Google Document.

##### `document_name: str`

The name of the Google Document.

### AuthenticationHelper Class

Helper class for authenticating with Google APIs.

#### Constructor

```python
AuthenticationHelper(service_account_file: str)
```

- **service_account_file**: Path to the Google service account JSON key file

#### Methods

##### `authenticate() -> None`

Authenticates with Google API using the service account credentials.

##### `async authenticate_async() -> None`

Asynchronous version of authenticate().

### Utility Functions

#### `convert_markdown_to_docx(markdown_text: str, title: str = "Document") -> Tuple[BytesIO, int]`

Converts Markdown content to DOCX format.

- **markdown_text**: Markdown content to convert
- **title**: Title for the document (default: "Document")
- **Returns**: A tuple containing a BytesIO object with the DOCX content and the file size

## Advanced Usage

### Document Creation with Sharing

```python
import asyncio
from docorator import Docorator

async def main():
    # Create and share a document with specific users
    doc = Docorator(
        'service-account-key.json',
        document_name="Team Project",
        email_addresses=["team1@example.com", "team2@example.com"]
    )

    await doc.initialize()
    print(f"Document created and shared: {doc.url()}")

asyncio.run(main())
```

### Export and Update Workflow

```python
import asyncio
from docorator import Docorator

async def main():
    doc = Docorator('service-account-key.json', document_id="your-doc-id-here")
    await doc.initialize()

    # Export current content
    markdown = await doc.export_as_markdown()

    # Modify the content
    modified_markdown = markdown.replace("# Original Title", "# New Title")
    modified_markdown += "\n\n## New Section\nThis section was added programmatically."

    # Update the document
    await doc.update_from_markdown(modified_markdown)

asyncio.run(main())
```

### Leveraging Caching

The Docorator class inherits from JSONCache (via Cacherator), which provides persistent caching. This means that document IDs and other properties are cached between program executions.

```python
import asyncio
from docorator import Docorator

async def main():
    # First run: will find or create the document
    doc1 = Docorator('service-account-key.json', document_name="Persistent Doc")
    await doc1.initialize()
    print(f"Document ID: {doc1.document_id}")

    # Second run: will use cached document ID
    doc2 = Docorator('service-account-key.json', document_name="Persistent Doc")
    # No need to call initialize() if you only need the cached document_id
    print(f"Cached document ID: {doc2.document_id}")

    # Clear cache if needed
    doc3 = Docorator('service-account-key.json', document_name="Persistent Doc", clear_cache=True)
    # Now initialize will search for the document again
    await doc3.initialize()

asyncio.run(main())
```

## Getting a Google Service Account

To use Docorator, you need a Google Service Account:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Docs API and Google Drive API
4. Go to "APIs & Services" > "Credentials"
5. Click "Create Credentials" > "Service Account"
6. Fill in the details and create the account
7. Create a key for the service account (JSON format)
8. Download the key file and use its path in the `service_account_file` parameter

## License

MIT License