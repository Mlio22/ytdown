from threading import Thread

# get the exact video that user wants
def getvideoorder(query):
    properties = query.getproperties()
    if properties['query_list'].checkquery(query):
        video_query = properties['video']

        message_text = properties['message'].content

        try:
            message_text = int(message_text) - 1
            if message_text <= video_query.getlistlength():
                video_query.setexactvideo(message_text)

                downloadthread = Thread(target=video_query.download, daemon=True)
                query.addthread(downloadthread)

                downloadthread.start()

        finally:
            return None


def getlangfromuser(query):
    properties = query.getproperties()
    if properties['query_list'].checkquery(query):
        sub_query = properties['sub']
        message_text = properties['message'].content

        try:
            print("here")
            message_text = int(message_text) - 1
            if message_text <= sub_query.getlanglength():
                print("here")
                sub_query.setlangfromuser(message_text)
                sub_query.checksubrequirements()
        finally:
            return None


def gettypefromuser(query):
    properties = query.getproperties()
    if properties['query_list'].checkquery(query):
        sub_query = properties['sub']
        message_text = properties['message'].content

        try:
            message_text = int(message_text) - 1
            if message_text <= 3:
                sub_query.settypefromuser(message_text)
                print('downloading')
                sub_query.checksubrequirements()
        finally:
            return None
