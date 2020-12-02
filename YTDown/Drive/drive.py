from pydrive.drive import GoogleDrive
import ntpath
from .credentials.credential import authenticate

gauth = authenticate()
drive = GoogleDrive(gauth)


def uploadfile(filepath, folderid):
    _, title = ntpath.split(filepath)
    file = drive.CreateFile(
        {'title': title, 'parents': [{'id': folderid}]}
    )

    file.SetContentFile(filepath)
    file.Upload()

    file.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })

    return file
