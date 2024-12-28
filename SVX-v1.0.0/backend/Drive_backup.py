from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os


def upload_to_google_drive(file_name):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r"C:\Users\User\Desktop\workspace2\SVX\SVX-v1.0.0\credentials.json", SCOPES
                
            )
            creds = flow.run_local_server(port= 0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build("drive", "v3", credentials = creds)
        response = service.files().list(
            q="name='BackupFolder' and mimeType='application/vnd.google-apps.folder'",
            spaces = 'drive'
        ).execute()

        if not response['files']:
            file_metadata = {
                "name" : "BackupFolder",
                "mimeType" : "application/vnd.google-apps.folder"
            }
            file = service.files().create(body = file_metadata, fields = "id").execute()
            folder_id = file.get('id')
        else:
            folder_id = response['files'][0]['id']

        for file in os.listdir('backupfiles'):
            file_metadata = {
                "name" : file_name,
                "parents" : [folder_id]
            }
            media = MediaFileUpload(f"backupfiles/{file_name}")
            upload_file = service.files().create(body=file_metadata, media_body= media, fields="id").execute()
    except HttpError as e:
        print("Error: " + str(e))
    

def upload_to_gdrive_by_key(file_name):
    #google drive api
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    #google drive key
    SERVICE_ACCOUNT_FILE = "credskey.json"
    #google drive folder id
    PARENT_ID_FOLDER = "19bDsCLLed5q9Qe8-aKhGoN1jeaPHrxde"

    #authenticate to google drive
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : "Name",
        'parents' : [PARENT_ID_FOLDER]
    }

    file = service.files().create(
        body = file_metadata,
        media_body = file_name
    ).execute()