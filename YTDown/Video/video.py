from pytube import YouTube
from YTDown.utils import customizemessage, bytetomb
from discord import File
from YTDown.Drive.drive import uploadfile
from YTDown.Drive.db.db import DB_VIDEO_FOLDER_ID
import asyncio


class VideoQuery:
    def __init__(self, message, videourl, flags, periodlist, query, currentloop):
        self._message = message
        self._video_url = videourl
        self._flags = flags
        self._period_list = periodlist
        self._query = query
        self._current_loop = currentloop

        # filter vars

        self._res = None
        self._output_type = None
        self._exact_video = None
        self._file_path = None
        self._fileid = None

        self._setflags()

        self._yt_video = YouTube(self._video_url)

        self._video_list = self._yt_video.streams
        self._thumbnail = self._yt_video.thumbnail_url
        self._video_title = self._yt_video.title

        self._filterlist()

    def _setflags(self):
        for flag in self._flags:
            if flag.startswith("-res="):
                self._res = flag.split('-res=')[1]
            if flag.startswith("-outputtype="):
                self._output_type = flag.split("-outputtype=")[1]

    def _filterlist(self):
        # filter to progressive type only
        self._video_list = self._video_list.filter(progressive=True)

        if self._res is not None:
            self._video_list = self._video_list.filter(res=self._res)

        if self._output_type is not None:
            self._video_list = self._video_list.filter(subtype=self._output_type)

    def showinfo(self):
        if len(self._video_list) > 0:
            self._showlist()
        else:
            self._shownone()

    def setcurrentloop(self, currentloop):
        self._current_loop = currentloop

    def getcurrentloop(self):
        return self._current_loop

    def getlistlength(self):
        return len(self._video_list)

    def setexactvideo(self, index):
        self._exact_video = self._video_list[index]
        self._video_title += "-{}".format(self._exact_video.resolution)

    def _showlist(self):
        message = "Nomor|Tipe|Resolusi|Ukuran|\n"
        for number, data in enumerate(self._video_list):
            message += "{}|{}|{}|{}|\n".format(number + 1, data.subtype, data.resolution, bytetomb(data.filesize))
        message = customizemessage(message)
        message = "```{}```".format(message)

        asyncio.run_coroutine_threadsafe(self._message.channel.send(message), self._current_loop)

    def _shownone(self):
        asyncio.run_coroutine_threadsafe(self._message.channel.send("No data available"), self._current_loop)

    def download(self):
        print("downloading file")

        if not self._query.iscancelled():
            self._file_path = self._exact_video.download(
                skip_existing=False,
                output_path="../cache",
                filename=self._video_title
            )

            print("downloaded")

            self.upload()

    def upload(self):
        if not self._query.iscancelled():
            print("uploading")
            if bytetomb(self._exact_video.filesize) <= 8.0:
                asyncio.run_coroutine_threadsafe(
                    self._message.channel.send("sending file... please wait"),
                    self._current_loop
                )

                asyncio.run_coroutine_threadsafe(
                    self._message.channel.send(file=File(self._file_path)),
                    self._current_loop
                )
            else:
                asyncio.run_coroutine_threadsafe(
                    self._message.channel.send("sending to drive... please wait"),
                    self._current_loop
                )

                self._fileid = uploadfile(self._file_path, DB_VIDEO_FOLDER_ID)['id']
                print("uplaoded")
                asyncio.run_coroutine_threadsafe(self._message.channel.send(
                    "https://drive.google.com/u/0/uc?id={}&export=download".format(self._fileid)
                ), self._current_loop)

                self._period_list.addperiod(self._fileid)
