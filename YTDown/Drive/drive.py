from pydrive.drive import GoogleDrive
from .credentials.credential import authenticate
import os
import ntpath

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


def deletebyid(fileid):
    """
    deletes google drive file by its file id

    :param fileid: google drive file id (str)
    :return: None
    """
    try:
        file = drive.CreateFile({'id': fileid})
        file.Delete()
    except Exception as error:
        pass


def deletebyname(filepath):
    """
    deletes local cache file by its filepath

    :param filepath: name of the file (str)
    :return: None
    """

    try:
        os.remove(filepath)
    except FileNotFoundError as error:
        print(error)
