import asyncio
from docorator import Docorator


async def main():
    # Initialize with document ID
    doc = Docorator('service-account-key.json', document_name="Der Hobbit")
    await doc.initialize()
    #document = await doc.get_document()
    markdown_content = await doc.export_as_markdown()
    print(markdown_content)
    markdown_content = "# Title\nThis is a test with an ![image](http://example.com/img.jpg)"
    success = await doc.update_from_markdown(markdown_content)
    print(success)


asyncio.run(main())