# NOTE: This file is for local use only. DO NOT use it in Streamlit Cloud.
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def download_from_drive(folder_id='1S0d8FCFxDRih4KDBsKuUO8G_Q2d3gRr5'):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    if not os.path.exists('documents'):
        os.makedirs('documents')

    file_list = drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false"
    }).GetList()

    print(f"Found {len(file_list)} files. Downloading...")
    for file in file_list:
        file_title = file['title']
        file.GetContentFile(os.path.join('documents', file_title))
        print(f"Downloaded: {file_title}")
    print("All files downloaded to 'documents' folder.")

# Uncomment to use locally:
# download_from_drive()
