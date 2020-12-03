import requests
from abc import ABC, abstractmethod
from operator import itemgetter
from YTDown.Sub.ass import utils
from YTDown.Sub import utils as commonutils


class Subtitle(ABC):
    def __init__(self, url):
        self._url = url + "&fmt=json3&xorb=2&xobt=3&xovt=3"
        self._caption_json = requests.get(self._url).json()

        self._events = None

        self._subtitle = ""

        self._getcaptionlist()

    def _getcaptionlist(self):
        self._events = self._caption_json['events']

    @abstractmethod
    def _convert(self):
        pass


class AssSubtitle(Subtitle):
    def __init__(self, url):
        super().__init__(url)

        self.__isassable = True

        self.__pens = []
        self.__win_styles = []
        self.__win_positions = []

    def __parsecaption(self):
        self.__pens = self._caption_json['pens']
        self.__win_styles = self._caption_json['wsWinStyles']
        self.__win_positions = self._caption_json['wpWinPositions']

    def __checklist(self):
        self.__parsecaption()

        penslen = len(self.__pens)
        wslen = len(self.__win_styles)
        wplen = len(self.__win_positions)

        if penslen == wslen and wslen == wplen and wplen == 0:
            self.__isassable = False

    @property
    def isassable(self):
        return self.__isassable

    def _convert(self):
        pass


class SrtSubtitle(Subtitle):
    def __init__(self, url):
        super().__init__(url)
        self._convert()
        self._showsubtitle()

    def _showsubtitle(self):
        print(self._subtitle)

    def _convert(self):
        subtitle_counter = 1
        for index, event in enumerate(self._events):
            first_text = self._events[index - 1]['segs'][0]['utf8']
            second_text = self._events[index]['segs'][0]['utf8']

            if (index > 0 and first_text != second_text) or index == 0:
                start_time, duration = itemgetter('tStartMs', 'dDurationMs')(event)

                self._subtitle += "{}\n{} --> {}\n{}\n\n".format(
                    subtitle_counter,
                    commonutils.getsrttime(start_time),
                    commonutils.getsrttime(start_time + duration),
                    second_text
                )
                subtitle_counter += 1


class TxtSubtitle(Subtitle):
    def __init__(self, url):
        super().__init__(url)
        self._convert()
        self._showsubtitle()

    def _showsubtitle(self):
        print(self._subtitle)

    def _convert(self):
        for index, event in enumerate(self._events):
            first_text = self._events[index - 1]['segs'][0]['utf8']
            second_text = self._events[index]['segs'][0]['utf8']

            if (index > 0 and first_text != second_text) or index == 0:
                self._subtitle += "{}\n".format(
                    self._events[index]['segs'][0]['utf8']
                )


# debug
if __name__ == '__main__':
    # srt = SrtSubtitle("https://www.youtube.com/api/timedtext?v=DlyG6MAKUOA&xorp=true&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1607014543&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cxorp%2Cxoaf&signature=62B4F8E71A764856C1C2A319AC23FCEB3FFC4988.CDAE9F6565AD012F802FB4241DD73A6D127B5916&key=yt8&lang=id&fmt=json3&xorb=2&xobt=3&xovt=3")
    txt = TxtSubtitle("https://www.youtube.com/api/timedtext?v=DlyG6MAKUOA&xorp=true&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1607014543&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cxorp%2Cxoaf&signature=62B4F8E71A764856C1C2A319AC23FCEB3FFC4988.CDAE9F6565AD012F802FB4241DD73A6D127B5916&key=yt8&lang=id&fmt=json3&xorb=2&xobt=3&xovt=3")

