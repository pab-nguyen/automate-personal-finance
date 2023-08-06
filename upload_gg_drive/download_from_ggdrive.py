# %%
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
gauth = GoogleAuth()      
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "./upload_gg_drive/client_secrets.json"
drive = GoogleDrive(gauth)
gauth.LoadCredentialsFile("./upload_gg_drive/credentials.json")

# %%
file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('19HgocA5Cb4QWDHXdD5YDqRg7sxjvIdLA')}).GetList()

for file in file_list:
	print('title: %s, id: %s' % (file['title'], file['id']))
	gfile = drive.CreateFile({'id': file['id']})
	gfile.GetContentFile("./data/other_input/"+file['title'])



