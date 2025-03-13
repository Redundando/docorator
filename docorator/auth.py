from typing import Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from logorator import Logger
from .exceptions import AuthenticationError


class GoogleAuth:
    def __init__(self, keyfile_path: str) -> None:
        self.keyfile_path = keyfile_path
        self.credentials = None
        self.docs_service = None
        self.drive_service = None
        self._authenticate()

    @Logger()
    def _authenticate(self) -> None:
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                self.keyfile_path,
                scopes=['https://www.googleapis.com/auth/documents',
                        'https://www.googleapis.com/auth/drive']
            )
            self.docs_service = build('docs', 'v1', credentials=self.credentials)
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
        except Exception as e:
            raise AuthenticationError(f"Failed to authenticate: {str(e)}")

    @Logger()
    def get_docs_service(self) -> Any:
        if not self.docs_service:
            self._authenticate()
        return self.docs_service

    @Logger()
    def get_drive_service(self) -> Any:
        if not self.drive_service:
            self._authenticate()
        return self.drive_service