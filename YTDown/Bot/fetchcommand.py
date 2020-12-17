from YTDown.Video.video import VideoQuery
from YTDown.Sub.sub import SubQuery


# video functions

def fetchyoutubevideodata(query):
    properties = query.getproperties()
    querylist = properties['query_list']
    if querylist.checkquery(query):
        print("creating video data")
        video = VideoQuery(
            properties['message'],
            properties['url'],
            properties['flags'],
            properties['period_list'],
            query,
            properties['current_loop']
        )

        if not query.iscancelled or not query.isinprocess:
            query.setproperty('video', video)
            video.showinfo()


def fetchyoutubesubdata(query):
    properties = query.getproperties()
    querylist = properties['query_list']
    if querylist.checkquery(query):
        print("creating subtitle data")
        sub = SubQuery(
            properties['message'],
            properties['url'],
            properties['flags'],
            properties['period_list'],
            query,
            currentloop=properties['current_loop']
        )

        if not query.iscancelled:
            query.setproperty('sub', sub)
            sub.checksubrequirements()
