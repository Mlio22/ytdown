from pydrive.drive import GoogleDrive
from YTDown.Drive.credentials.credential import authenticate
from YTDown.Drive.utils import searchorcreatedrivebyid
from YTDown.Drive.credentials.keys import FOLDER_ID, SAVED_FILES_ID
from datetime import datetime

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


def savedpreviousfiles():
    """
    gets previous saved files data in GD's saved_datas.txt
    :return: list of previous saved files (list(dict))
    """
    saved_data = db_file
    saved_data = saved_data.GetContentString()

    parsedlist = []
    print(saved_data, type(saved_data))
    if saved_data != "":
        saved_data_lists = saved_data.split('\n')
        for saved_data_list in saved_data_lists:
            filetype, fileid, filename, timestampgd, timestamplocal = saved_data_list.split('|')

            if timestampgd != 'None':
                timestampgd = datetime.strptime(timestampgd, "%d %m %y %H:%M:%S")
            else:
                timestampgd = ''

            if timestamplocal != 'None':
                timestamplocal = datetime.strptime(timestamplocal, "%d %m %y %H:%M:%S")
            else:
                timestamplocal = ''

            parsedlist.append({
                'filetype': filetype,
                'fileid': fileid,
                'filename': filename,
                'timestampgd': timestampgd,
                'timestamplocal': timestamplocal
            })

    return parsedlist


# debug
if __name__ == "__main__":
    db_file.SetContentString("A")
    db_file.Upload()