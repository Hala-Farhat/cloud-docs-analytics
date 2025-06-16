import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def ensure_documents_folder():
    if not os.path.exists('documents'):
        os.makedirs('documents')

def download_from_drive(folder_id='1S0d8FCFxDRih4KDBsKuUO8G_Q2d3gRr5'):
    ensure_documents_folder()

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.json")
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false"
    }).GetList()

    for file in file_list:
        file_title = file['title']
        file_path = os.path.join('documents', file_title)
        if not os.path.exists(file_path):  # لتجنب التكرار
            file.GetContentFile(file_path)

def upload_to_drive(file_path, folder_id):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.json")
    drive = GoogleDrive(gauth)

    file_name = os.path.basename(file_path)
    file_drive = drive.CreateFile({
        'title': file_name,
        'parents': [{'id': folder_id}]
    })
    file_drive.SetContentFile(file_path)
    file_drive.Upload()

    return f"✅ Uploaded '{file_name}' to Google Drive."
