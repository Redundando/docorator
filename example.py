from docorator import Docorator
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from docx import Document

def main():
    # Initialize with your service account key file and email for sharing
    key_path = "service-account-key.json"
    email = "klojarve@audible.de"  # Email to share documents with
    doco = Docorator(keyfile_path="service-account-key.json", email="klojarve@audible.de", document_name="Example Document")
    doco.load()
    # Get or create a document named "Example Document"
    #document = doc_manager.get_document("Example Document")

    print(doco.as_markdown())



    # Save the document back to Google Docs
    doco.save("# This is a headline\n\n## Part 1\n\nHello World\\!")


if __name__ == "__main__":
    main()