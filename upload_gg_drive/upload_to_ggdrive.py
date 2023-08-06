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
file_dict = {}
for file in file_list:
	print('title: %s, id: %s' % (file['title'], file['id']))
	file_dict[file['title']] = file['id']
	
# %%
files = os.listdir('./data/other_input/') 
files

# %%
for upload_file in files:
	try:
		gfile = drive.CreateFile({'id': file_dict[upload_file]})
		# Read file and set it as the content of this instance.
		gfile.SetContentFile('./data/other_input/'+str(upload_file))
		gfile.Upload() # Upload the file.
		gfile.content.close()
	except:
		pass


