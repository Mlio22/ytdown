from YTDown.Drive.drive import drive


def searchorcreatedrivebyid(fileid):
    """
    searches a Google drive file or creates it if don't exist
    :param fileid:
    :return: a google drive file object (dict)
    """
    file = drive.CreateFile({'id': fileid})
    return file
