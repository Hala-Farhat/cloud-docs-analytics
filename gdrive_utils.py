import os
import io
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# إعداد الاتصال عبر Google Drive API باستخدام streamlit secrets
SCOPES = ['https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gdrive"], scopes=SCOPES
)

drive_service = build('drive', 'v3', credentials=credentials)

def download_from_drive(folder_id, local_folder='documents'):
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    query = f"'{folder_id}' in parents and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    for file in files:
        file_id = file['id']
        file_name = file['name']
        local_path = os.path.join(local_folder, file_name)

        if not os.path.exists(local_path):
            request = drive_service.files().get_media(fileId=file_id)
            fh = io.FileIO(local_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

def upload_to_drive(file_path, folder_id):
    file_name = os.path.basename(file_path)

    # Check if file already exists in the folder
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    response = drive_service.files().list(q=query, spaces='drive', fields='files(id)').execute()
    existing_files = response.get('files')
    if existing_files:
        file_id = existing_files[0]['id']
        return f"⚠️ File already exists in Drive: {file_name}", file_id

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return f"✅ Uploaded to Drive: {file_name}", uploaded_file.get('id')
