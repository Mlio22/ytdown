from YTDown.Drive.drive import drive


def createfolder(name):
    folder = drive.CreateFile({
        'title': name,
        'mimeType': "application/vnd.google-apps.folder"
    })
    folder.Upload()

    return folder


def createfile(name, permissions=None, parentid=None):
    file = drive.CreateFile({
        'title': name,
        'parents': [{'id': parentid}]
    })

    if permissions is not None:
        file.InsertPermission(permissions)

    file.Upload()
    return file


def searchorcreatedrivebyid(fileid):
    file = drive.CreateFile({'id': fileid})
    return file


def deletebyid(fileid):
    try:
        file = drive.CreateFile({'id': fileid})
        file.Delete()
    finally:
        pass
