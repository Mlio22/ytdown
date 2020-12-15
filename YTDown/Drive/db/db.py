from pydrive.drive import GoogleDrive
from YTDown.Drive.credentials.credential import authenticate
from YTDown.Drive.utils import searchorcreatedrivebyid
from YTDown.Drive.credentials.keys import FOLDER_ID, SAVED_FILES_DIR
from datetime import datetime

DB_MAIN_FOLDER_ID = FOLDER_ID['main']
DB_SUB_FOLDER_ID = FOLDER_ID['sub']
DB_VIDEO_FOLDER_ID = FOLDER_ID['video']
DB_ALL_FOLDER_ID = FOLDER_ID['all']

# authenticate
gauth = authenticate()

drive = GoogleDrive(gauth)

main_folder = searchorcreatedrivebyid(DB_MAIN_FOLDER_ID)
sub_folder = searchorcreatedrivebyid(DB_SUB_FOLDER_ID)
video_folder = searchorcreatedrivebyid(DB_VIDEO_FOLDER_ID)
all_folder = searchorcreatedrivebyid(DB_ALL_FOLDER_ID)


def readdbfile():
    try:
        saved_data = open(SAVED_FILES_DIR, encoding='utf-8').read()
    except FileNotFoundError:
        open(SAVED_FILES_DIR, 'w').close()
        saved_data = open(SAVED_FILES_DIR, encoding='utf-8').read()

    return saved_data


def rewritedbfile(content):
    db_file = open(SAVED_FILES_DIR, 'w', encoding='utf-8')
    db_file.write(content)

    print("file rewrited")


def savedpreviousfiles():
    """
    gets previous saved files data in GD's saved_datas.txt
    :return: list of previous saved files (list(dict))
    """

    saved_data = readdbfile()

    parsedlist = []
    print(saved_data, type(saved_data))
    if saved_data != "":
        saved_data_lists = saved_data.split('\n')
        for saved_data_list in saved_data_lists:
            filetype, fileid, filepath, timestampgd, timestamplocal = saved_data_list.split('|')

            if timestampgd != 'None':
                timestampgd = datetime.strptime(timestampgd, "%d %m %y %H:%M:%S")

            if timestamplocal != 'None':
                timestamplocal = datetime.strptime(timestamplocal, "%d %m %y %H:%M:%S")

            parsedlist.append({
                'filetype': filetype,
                'fileid': fileid,
                'filepath': filepath,
                'timestampgd': timestampgd,
                'timestamplocal': timestamplocal
            })

    return parsedlist


# debug
if __name__ == "__main__":
    a = savedpreviousfiles()
    print(a)
