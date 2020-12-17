from YTDown.Bot.requestquery import RequestQuery
from YTDown.Bot.command import getvideoorder
from YTDown.Drive.db.db import DB_VIDEO_FOLDER_ID
from YTDown.utils import customizemessage, bytetomb


class VideoQuery(RequestQuery):
    def __init__(self, message, videourl, flags, periodlist, query, currentloop):
        super().__init__(message, videourl, flags, periodlist, query, currentloop)

        # request-related vars
        self._gd_folderid = DB_VIDEO_FOLDER_ID
        self._request_type = 'video'

        # query props
        self._list = self._youtube_object.streams

        # filter flags
        self.__res_flag = None
        self.__output_type_flag = None

        # video props
        self.__video_resolution = None

        # filter videos
        self._setflags()
        self.__filterlist()

    def _setflags(self):
        for flag in self._flags:
            if flag.startswith("-res="):
                self._res_flag = flag.split('-res=')[1]
            if flag.startswith("-videotype="):
                self._output_type_flag = flag.split("-videotype=")[1]

    def __filterlist(self):
        # filter to progressive type only
        # todo: gabungkan file audio dan video secara manual (non progressive)
        # self._list = self._list.filter(progressive=True)

        if self.__res_flag is not None:
            self._list = self._list.filter(res=self.__res_flag)

        if self.__output_type_flag is not None:
            self._list = self._list.filter(subtype=self.__output_type_flag)

    def showinfo(self):
        if len(self._list) > 0:
            self.__showlist()
            self._query.setqueryfunction(getvideoorder)
        else:
            self.__shownovideo()

    def getlistlength(self):
        return len(self._list)

    def setexactvideo(self, index):
        print("lol1")
        self._exact = self._list[index]
        self.__video_resolution = self._exact.resolution
        self._filesize = bytetomb(self._exact.filesize)

        # set file name
        self._filename = "{}-{}.{}".format(
            self._youtube_title,
            self.__video_resolution,
            self._exact.subtype
        ).replace("/", "").replace("\\", "")

    def __showlist(self):
        message = "Nomor|Tipe|Resolusi|Ukuran|\n"
        for number, data in enumerate(self._list):
            message += "{}|{}|{}|{}|\n".format(number + 1, data.subtype, data.resolution, bytetomb(data.filesize))
        message = customizemessage(message)
        message = "```{}```".format(message)

        self._sendtexttodiscord(message)

    def __shownovideo(self):
        self._sendtexttodiscord("No video available")
        self._query.videofinished()

    def download(self):
        VIDEO_DIR = "C:\\Users\\Acer\\Documents\\TELKOM TUGAS\\python_dev\\ytdown-dc-bot\\YTDown\Bot\../cache/video/"
        self._filepath = "{}{}".format(VIDEO_DIR, self._filename)

        print(self._filepath)

        super().download()

    def _savefile(self):
        if not self._query.iscancelled:
            self._filepath = self._exact.download(
                skip_existing=True,
                output_path="../cache/video/",
                filename=self._filename.replace(self._exact.subtype, "")
            )

            print(self._filepath)

            print("downloaded")

    def _queryfinished(self):
        self._query.videofinished()

