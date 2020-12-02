import asyncio
from YTDown.Video.video import Video
from threading import Thread


# video functions

def fetchyoutubedata(query):
    properties = query.getproperties()
    querylist = properties['query_list']
    if querylist.checkquery(query):
        print("creating video")
        video = Video(
            properties['message'],
            properties['url'],
            properties['flags'],
            properties['period_list'],
            query,
            currentloop=properties['current_loop']
        )

        if not query.iscancelled():
            print("hello")
            query.setproperty('video', video)
            print("setting video")

            if video.getlistlength() > 0:
                query.setqueryfunction(getvideoorder)

            video.showinfo()


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
