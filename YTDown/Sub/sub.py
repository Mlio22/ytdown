from pytube import YouTube
import asyncio


class SubQuery:
    def __init__(self, message, suburl, flags, periodlist, query, currentloop):
        self._message = message
        self._sub_url = suburl
        self._flags = flags
        self._period_list = periodlist
        self._query = query
        self._current_loop = currentloop

        # filter vars

        self._lang = ""

        self._setflags()

        self._ytsub = YouTube(self._sub_url)
        self._caption_list = self._ytsub.captions
        self._thumbnail = self._ytsub.thumbnail_url
        self._sub_title = self._ytsub.title

        self._exact_caption = None

        self._sub = None
        self._sub_type = None
        self.isdownloadable = False

        self._filterlist()
        self.checkisdownloadable()

    def _setflags(self):
        for flag in self._flags:
            if flag.startswith('-lang='):
                self._lang = flag.split('-lang=')[1]
            if flag.startswith('-type='):
                subtype = flag.split('-type=')[1]
                self.setsubtype(subtype)

    def _filterlist(self):
        if self._lang is not None:
            for caption in self._caption_list:
                if caption.code == self._lang:
                    self._exact_sub = caption

    def setsubtype(self, subtype):
        self._sub_type = subtype

    def checkisdownloadable(self):
        if self._exact_caption is not None and self._sub_type is not None:
            if self._sub_type == 'ass':

