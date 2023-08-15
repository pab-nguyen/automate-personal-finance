# %%
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import datetime
import pytz

# %%
# authentication
gauth = GoogleAuth()      
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "./upload_gg_drive/client_secrets.json"
drive = GoogleDrive(gauth)
gauth.LoadCredentialsFile("./upload_gg_drive/credentials.json")

# %%
#get drive files list and local file list
drive_files = drive.ListFile({'q': "'{}' in parents and trashed=false".format('19HgocA5Cb4QWDHXdD5YDqRg7sxjvIdLA')}).GetList()
local_files = os.listdir('./data/other_input/') 

# %%
# go through each file name in drive
for file in drive_files:
    #get drive files names
    drive_file_id = file['id']
    drive_file_name = file['title']
    #get local file path	
    local_file_path = os.path.join('./data/other_input/', drive_file_name)

    #check if drive file in local folder
    if drive_file_name in local_files:
        #get drive modified time, changing timezone
        modified_time = file['modifiedDate']
        utc_time = datetime.datetime.strptime(modified_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        utc_time = utc_time.replace(tzinfo=pytz.UTC)

        local_timezone = pytz.timezone('America/New_York')  # Replace with your local timezone
        local_time = utc_time.astimezone(local_timezone)

        #get modified time for both drive and local        
        drive_last_modified = local_time.replace(tzinfo=None)
        local_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(local_file_path))

        #if local file has newer updated time
        if local_last_modified > drive_last_modified:
                # Upload local file to Google Drive
                drive_file = drive.CreateFile({'id': drive_file_id})
                drive_file.SetContentFile(local_file_path)
                drive_file.Upload()
                print(f"Uploaded {drive_file_name} to Google Drive")
        #if drive file has newer updated time
        elif drive_last_modified > local_last_modified:
                # Download Google Drive file to local
                drive_file = drive.CreateFile({'id': drive_file_id})
                drive_file.GetContentFile(local_file_path)
                print(f"Downloaded {drive_file_name} from Google Drive")
        else:
            # Download Google Drive file to local since it doesn't exist locally
            drive_file = drive.CreateFile({'id': drive_file_id})
            drive_file.GetContentFile(local_file_path)
            print(f"Downloaded {drive_file_name} from Google Drive")

	