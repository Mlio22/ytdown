from pytube import YouTube
from discord import File
from YTDown.Sub.ass.AssSubtitle import AssSubtitle
from YTDown.Sub.srt.SrtSubtitle import SrtSubtitle
from YTDown.Sub.txt.TxtSubtitle import TxtSubtitle
from YTDown.utils import customizemessage, bytetomb
from YTDown.Bot.command import getlangfromuser, gettypefromuser
from YTDown.Drive.drive import uploadfile
from YTDown.Drive.db.db import DB_SUB_FOLDER_ID
import os

import asyncio

SUB_TYPES = ['ass', 'srt', 'txt']


class SubQuery:
    def __init__(self, message, suburl, flags, periodlist, query, currentloop):
        self._message = message
        self._sub_url = suburl
        self._flags = flags
        self._period_list = periodlist
        self._query = query
        self._current_loop = currentloop

        # filter vars

        self._lang = None
        self._sub_type = None

        self._setflags()

        self._ytsub = YouTube(self._sub_url)
        self._caption_list = self._ytsub.captions

        self._thumbnail = self._ytsub.thumbnail_url
        self._sub_title = self._ytsub.title.replace("/", "")
        self._sub_dir = None
        self._fileid = None

        self._exact_caption = None

        self._sub = None

    def _setflags(self):
        """
        set language and type by the flags
        :return: Nothing
        """
        for flag in self._flags:
            if flag.startswith('-lang='):
                lang = flag.split('-lang=')[1]
                self.setlang(lang)
            if flag.startswith('-type='):
                subtype = flag.split('-type=')[1]
                self.setsubtype(subtype)

    def setlang(self, lang):
        """
        filter
        :param lang:
        :return:
        """

        self._lang = lang

    def get_exact_caption(self):
        print(self._lang)
        if self._lang is not None:
            for caption in self._caption_list:
                if caption.code == self._lang:
                    self._exact_caption = caption
            if self._exact_caption is None:
                self.shownocaption()

    def shownocaption(self):
        asyncio.run_coroutine_threadsafe(
            self._message.channel.send("caption unavailable"),
            self._current_loop
        )

    def setsubtype(self, subtype):
        self._sub_type = subtype

    def selectlangmessage(self):
        message = "Nomor|Bahasa|\n"
        for number, caption in enumerate(self._caption_list):
            message += "{}|{} ({})|\n".format(number + 1, caption.name, caption.code)
        message = customizemessage(message)
        message = "```{}```".format(message)

        asyncio.run_coroutine_threadsafe(
            self._message.channel.send(message),
            self._current_loop
        )

    def selecttypemessage(self):
        message = "Nomor|Tipe Subtitle|\n"
        for number, _ in enumerate(SUB_TYPES):
            message += "{}|{}|\n".format(number + 1, SUB_TYPES[number])
        message = customizemessage(message)
        message = "```{}```".format(message)

        asyncio.run_coroutine_threadsafe(
            self._message.channel.send(message),
            self._current_loop
        )

    def download(self):
        if not self._query.iscancelled():
            if self._sub_type == "ass":
                self._sub = AssSubtitle(self._exact_caption.url)
            elif self._sub_type == "srt":
                self._sub = SrtSubtitle(self._exact_caption.url)
            elif self._sub_type == "txt":
                self._sub = TxtSubtitle(self._exact_caption.url)

        print('sub created')

        self._savefile()
        self._uploadfile()

    def _savefile(self):
        self._sub_title = "{} -{}.{}".format(
            self._sub_title, self._lang, self._sub_type
        )

        print(self._sub_title)

        self._sub_dir = "../cache/sub/{}/{}".format(
            self._sub_type, self._sub_title
        )
        is_file_exist = os.path.exists(self._sub_dir)

        if not is_file_exist:
            try:
                f = open(self._sub_dir, 'w', encoding='utf-8')
                f.write(self._sub.subtitle)
                f.close()
            except Exception as error:
                print(error)

    def _uploadfile(self):
        if bytetomb(os.path.getsize(self._sub_dir)) <= 8.0:
            asyncio.run_coroutine_threadsafe(
                self._message.channel.send("sending file... please wait"),
                self._current_loop
            )

            print(self._sub_title)
            asyncio.run_coroutine_threadsafe(
                self._message.channel.send(file=File(self._sub_dir, self._sub_title)),
                self._current_loop
            )
        else:
            asyncio.run_coroutine_threadsafe(
                self._message.channel.send("sending to drive... please wait"),
                self._current_loop
            )

            self._fileid = uploadfile(self._sub_dir, DB_SUB_FOLDER_ID)['id']
            asyncio.run_coroutine_threadsafe(self._message.channel.send(
                "https://drive.google.com/u/0/uc?id={}&export=download".format(self._fileid)
            ), self._current_loop)

            self._period_list.addperiod(self._fileid)

        print("saved in local")

    def getflags(self):
        return {
            "lang": self._lang,
            "type": self._sub_type
        }

    def getlanglength(self):
        return len(self._caption_list)

    def setlangfromuser(self, usernumber):
        for number, caption in enumerate(self._caption_list):
            if usernumber == number:
                self._lang = caption.code

    def settypefromuser(self, usernumber):
        self.setsubtype(SUB_TYPES[usernumber])

    def checksubrequirements(self):
        print(self._lang, self._sub_type)
        if self._lang is None:
            self.selectlangmessage()
            self._query.setqueryfunction(getlangfromuser)
        elif self._sub_type is None:
            self.selecttypemessage()
            self._query.setqueryfunction(gettypefromuser)
        else:
            self.get_exact_caption()
            self.download()
