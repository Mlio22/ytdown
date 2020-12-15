import asyncio
from abc import abstractmethod
from pytube import YouTube
from discord import File
from YTDown.Drive.drive import uploadfile


class RequestQuery:
    def __init__(self, message, videourl, flags, periodlist, query, currentloop):
        self._message = message
        self._video_url = videourl
        self._flags = flags
        self._period_list = periodlist
        self._query = query
        self._current_loop = currentloop

        # request-related vars
        self._gd_folderid = None
        self._request_type = None

        # file props
        self._filepath = None
        self._fileid = None
        self._filename = None
        self._filesize = None

        # youtube object props
        self._youtube_object = YouTube(self._video_url)
        self._youtube_title = self._youtube_object.title
        self._youtube_thumbnail = self._youtube_object.thumbnail_url

        # query props
        self._list = None
        self._exact = None

    @abstractmethod
    def _setflags(self):
        """
        sets flags for filtering list
        :return: None
        """
        pass

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def _savefile(self):
        pass

    def _upload(self):
        """
        Uploads subtitle to discord or drive if the size is beyond 8MB
        :return:None
        """
        if not self._query.iscancelled():
            if self._filesize <= 8.0:
                self._sendtexttodiscord("sending file to discord")
                self._sendfiletodiscord(self._filepath, self._filename)
            else:
                self._sendtexttodiscord("sending to drive... please wait")

                self._fileid = uploadfile(self._filepath, self._gd_folderid)['id']
                self._sendgdlinktodiscord(self._fileid)

        if not self._query.iscancelled():
            self._period_list.addnewperiod(self._request_type, self._filepath, self._fileid)

    def _sendtexttodiscord(self, text):
        asyncio.run_coroutine_threadsafe(
            self._message.channel.send(text),
            self._current_loop
        )

    def _sendfiletodiscord(self, filedir, title):
        asyncio.run_coroutine_threadsafe(
            self._message.channel.send(file=File(filedir, title)),
            self._current_loop
        )

    def _sendgdlinktodiscord(self, fileid):
        asyncio.run_coroutine_threadsafe(self._message.channel.send(
            "https://drive.google.com/u/0/uc?id={}&export=download".format(fileid)
        ), self._current_loop)


# debug
if __name__ == '__main__':
    yt = YouTube("https://www.youtube.com/watch?v=M7sr5zv1EkI").streams.first().download()

    print(yt)