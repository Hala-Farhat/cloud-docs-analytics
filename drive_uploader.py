from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# ✅ مصادقة Google Drive مع حفظ الاعتماد
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

# ✅ رفع ملف إلى مجلد محدد في Google Drive
def upload_to_drive(file_path, folder_id):
    drive = authenticate_drive()
    file_name = os.path.basename(file_path)

    # التأكد من عدم وجود الملف مسبقًا (لتجنب التكرار)
    existing = drive.ListFile({
        'q': f"title='{file_name}' and '{folder_id}' in parents and trashed=false"
    }).GetList()

    if existing:
        return f"⚠️ File already exists in Drive: {file_name}"

    file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    return f"✅ Uploaded to Drive: {file_name}"
