from pydrive.drive import GoogleDrive
from YTDown.Drive.credentials.credential import authenticate
from YTDown.Drive.utils import createfolder, createfile, searchorcreatedrivebyid
from YTDown.Drive.credentials.keys import FOLDER_ID, SAVED_FILES_ID

DB_MAIN_FOLDER_ID = FOLDER_ID['main']
DB_SUB_FOLDER_ID = FOLDER_ID['sub']
DB_VIDEO_FOLDER_ID = FOLDER_ID['video']
DB_ALL_FOLDER_ID = FOLDER_ID['all']

DB_SAVED_DATAS_ID = SAVED_FILES_ID

# authenticate
gauth = authenticate()

drive = GoogleDrive(gauth)

main_folder = searchorcreatedrivebyid(DB_MAIN_FOLDER_ID)
sub_folder = searchorcreatedrivebyid(DB_SUB_FOLDER_ID)
video_folder = searchorcreatedrivebyid(DB_VIDEO_FOLDER_ID)
all_folder = searchorcreatedrivebyid(DB_ALL_FOLDER_ID)

db_file = searchorcreatedrivebyid(DB_SAVED_DATAS_ID)


def parsesavedfile():
    saved_data = db_file
    saved_data = saved_data.GetContentString() or ""

    parsedlist = []
    if saved_data != "":
        saved_data_lists = saved_data.split('\n')
        saved_data_lists.remove(saved_data_lists[0])
        for saved_data_list in saved_data_lists:
            fileid, deadline = saved_data_list.split('|')
            parsedlist.append({
                'fileid': fileid,
                'deadline': deadline
            })

    return parsedlist


def getfolders():
    return {
        "main": main_folder,
        "sub": sub_folder,
        "video": video_folder,
        "all": all_folder
    }
