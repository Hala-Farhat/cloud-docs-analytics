from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# مصادقة Google
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

# رفع ملف إلى Google Drive داخل مجلد معين
def upload_to_drive(file_path, folder_id):
    drive = authenticate_drive()
    file_name = os.path.basename(file_path)
    file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    return f"✅ Uploaded to Drive: {file_name}"
