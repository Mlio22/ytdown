import os
from YTDown.Bot.requestquery import RequestQuery
from YTDown.Sub.ass.AssSubtitle import AssSubtitle
from YTDown.Sub.srt.SrtSubtitle import SrtSubtitle
from YTDown.Sub.txt.TxtSubtitle import TxtSubtitle
from YTDown.Bot.command import getlangfromuser, gettypefromuser
from YTDown.Drive.db.db import DB_SUB_FOLDER_ID
from YTDown.utils import customizemessage, bytetomb

SUB_TYPES = ['ass', 'srt', 'txt']


class SubQuery(RequestQuery):
    def __init__(self, message, videourl, flags, periodlist, query, currentloop):
        super().__init__(message, videourl, flags, periodlist, query, currentloop)

        # request-related vars
        self._gd_folderid = DB_SUB_FOLDER_ID
        self._request_type = 'sub'

        # query props
        self._list = self._youtube_object.captions

        # filter flags
        self.__lang_flag = None
        self.__sub_type_flag = None

        # subtitle props
        self.__lang = None
        self.__sub_type = None

        # parsed caption
        self.__subtitle = None

        # filter captions
        self._setflags()

    def _setflags(self):
        for flag in self._flags:
            if flag.startswith('-lang='):
                lang = flag.split('-lang=')[1]
                self.__setlang(lang)
            if flag.startswith('-subtype='):
                subtype = flag.split('-subtype=')[1]
                self.__setsubtype(subtype)

    def __setlang(self, lang):
        """
        filter
        :param lang:
        :return:
        """

        self.__lang = lang

    def __setsubtype(self, subtype):
        self.__sub_type = subtype

    def getexactcaption(self):
        """
        gets the exact caption from user's response to be parsed
        :return: None
        """
        if self.__lang is not None:
            for caption in self._list:
                if caption.code == self.__lang:
                    self._exact = caption
            if self._exact is None:
                self.__shownocaption()

    def __shownocaption(self):
        """
        Informs user that no caption available on that query
        :return: None
        """
        self._sendtexttodiscord("No caption available")

    def __selectlangmessage(self):
        """
        Informs user list of languages that available on that query
        and set query function to wait user's pick
        :return:
        """
        message = "Nomor|Bahasa|\n"
        for number, caption in enumerate(self._list):
            message += "{}|{} ({})|\n".format(number + 1, caption.name, caption.code)
        message = customizemessage(message)
        message = "```{}```".format(message)

        self._sendtexttodiscord(message)

        # sets query function
        self._query.setqueryfunction(getlangfromuser)

    def __selecttypemessage(self):
        """
        Informs user the list of subtitle types available
        and sets query function to wait user's pick
        :return:None
        """
        message = "Nomor|Tipe Subtitle|\n"
        for number, _ in enumerate(SUB_TYPES):
            message += "{}|{}|\n".format(number + 1, SUB_TYPES[number])
        message = customizemessage(message)
        message = "```{}```".format(message)

        self._sendtexttodiscord(message)

        # sets query function
        self._query.setqueryfunction(gettypefromuser)

    def getlanglength(self):
        return len(self._list)

    def setlangfromuser(self, usernumber):
        for number, caption in enumerate(self._list):
            if usernumber == number:
                self.__setlang(caption.code)

    def settypefromuser(self, usernumber):
        self.__setsubtype(SUB_TYPES[usernumber])

    def checksubrequirements(self):
        if self.__lang is None:
            self.__selectlangmessage()
        elif self.__sub_type is None:
            self.__selecttypemessage()
        else:
            self.getexactcaption()
            self.download()

    def download(self):
        """
        downloads the caption, saves it, and then uploads it
        :return: None
        """
        self.__parsecaption()
        self._savefile()
        self._upload()

        self._query.subfinished()

    def __parsecaption(self):
        """
        downloads the caption and parses it
        :return:
        """
        if not self._query.iscancelled():
            if self.__sub_type == "ass":
                self.__subtitle = AssSubtitle(self._exact.url)
            elif self.__sub_type == "srt":
                self.__subtitle = SrtSubtitle(self._exact.url)
            elif self.__sub_type == "txt":
                self.__subtitle = TxtSubtitle(self._exact.url)

        print('sub created')

    def _savefile(self):
        """
        saves subtitle file to cache
        :return: None
        """
        if not self._query.iscancelled():
            # sets filename of subtitle
            SUB_DIR = "C:\\Users\\Acer\\Documents\\TELKOM TUGAS\\python_dev\\ytdown-dc-bot\\YTDown\\cache\\sub\\{}\\"\
                .format(self.__sub_type)

            self._filename = "{}-{}.{}".format(self._youtube_title, self.__lang, self.__sub_type).replace("/", "").replace("\\", "")
            self._filepath = "{}{}".format(SUB_DIR, self._filename)

            print(self._filepath)

            is_file_exist = os.path.exists(self._filepath)
            print(self._filepath, self.__subtitle.subtitle)

            if not is_file_exist:
                try:
                    f = open(self._filepath, 'w', encoding='utf-8')
                    f.write(self.__subtitle.subtitle)
                    f.close()
                except Exception as error:
                    print(error)

            self._filesize = bytetomb(os.path.getsize(self._filepath))
            print("saved in local")
