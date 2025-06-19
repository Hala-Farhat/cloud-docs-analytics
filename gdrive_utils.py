import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# ✅ إجراء المصادقة باستخدام PyDrive وحفظ بيانات الاعتماد
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        # في أول مرة، يتم تسجيل الدخول عبر المتصفح
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # في حال انتهاء الجلسة، يتم تحديث الرمز
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

# ✅ رفع ملف إلى Google Drive داخل مجلد معين
def upload_to_drive(file_path, folder_id):
    drive = authenticate_drive()
    file_name = os.path.basename(file_path)

    # ✅ تحقق من أن الملف غير موجود مسبقًا لتجنب الازدواج
    query = f"title='{file_name}' and '{folder_id}' in parents and trashed=false"
    existing_files = drive.ListFile({'q': query}).GetList()

    if existing_files:
        return f"⚠️ File already exists in Drive: {file_name}"

    file_metadata = {'title': file_name, 'parents': [{'id': folder_id}]}
    file_drive = drive.CreateFile(file_metadata)
    file_drive.SetContentFile(file_path)
    file_drive.Upload()

    return f"✅ Uploaded to Drive: {file_name}"
