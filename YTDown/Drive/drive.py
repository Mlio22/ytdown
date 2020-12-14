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
    finally:
        pass


def deletebyname(filetype, filename):
    """
    deletes local cache file by its filetype and filename

    :param filetype: type of the file, opt: video/sub (str)
    :return: None
    """
    try:
        file_dir = "C:/Users/Acer/Documents/TELKOM TUGAS/python_dev/ytdown-dc-bot/YTDown/Bot/../cache/{}/{}".format(
            filetype, filename)
        os.remove(file_dir)
    except FileNotFoundError:
        pass
