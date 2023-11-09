# noinspection PyPackageRequirements
from googleapiclient.discovery import build

# noinspection PyPackageRequirements
from google.oauth2.service_account import Credentials

# Nếu sửa scope ở đây, xóa file token.json
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]
_creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
calendar_service = build("calendar", "v3", credentials=_creds)
sheets_service = build("sheets", "v4", credentials=_creds)
