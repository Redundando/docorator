from google.oauth2 import service_account
from googleapiclient.discovery import build
import asyncio


class AuthenticationHelper:
    def __init__(self, service_account_file: str):
        self.service_account_file = service_account_file
        self.credentials = None
        self.docs_service = None
        self.drive_service = None

    def authenticate(self) -> None:
        self.credentials = service_account.Credentials.from_service_account_file(self.service_account_file, scopes=['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive'])
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    async def authenticate_async(self) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.authenticate)