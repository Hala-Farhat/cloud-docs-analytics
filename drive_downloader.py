from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


gauth = GoogleAuth()
gauth.LocalWebserverAuth()


drive = GoogleDrive(gauth)



folder_id = '1S0d8FCFxDRih4KDBsKuUO8G_Q2d3gRr5'

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
