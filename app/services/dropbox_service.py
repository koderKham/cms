import os
import dropbox
from dropbox.exceptions import ApiError
from config import Config


class DropboxService:
    def __init__(self):
        self.dbx = dropbox.Dropbox(
            app_key=Config.DROPBOX_APP_KEY,
            app_secret=Config.DROPBOX_APP_SECRET,
            oauth2_refresh_token=Config.DROPBOX_REFRESH_TOKEN
        )

    def upload_file(self, file_path, dropbox_path):
        """Upload a file to Dropbox"""
        with open(file_path, 'rb') as f:
            try:
                self.dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
                return True, dropbox_path
            except ApiError as e:
                return False, str(e)

    def download_file(self, dropbox_path, download_path):
        """Download a file from Dropbox"""
        try:
            self.dbx.files_download_to_file(download_path, dropbox_path)
            return True, download_path
        except ApiError as e:
            return False, str(e)

    def list_folder(self, folder_path):
        """List contents of a folder"""
        try:
            result = self.dbx.files_list_folder(folder_path)
            files = []
            for entry in result.entries:
                files.append({
                    'name': entry.name,
                    'path': entry.path_display,
                    'is_folder': isinstance(entry, dropbox.files.FolderMetadata)
                })
            return True, files
        except ApiError as e:
            return False, str(e)

    def create_folder(self, folder_path):
        """Create a folder in Dropbox"""
        try:
            self.dbx.files_create_folder_v2(folder_path)
            return True, folder_path
        except ApiError as e:
            return False, str(e)