import requests
from abc import ABC, abstractmethod

class Subtitle(ABC):
    def __init__(self, url):
        self._url = url + "&fmt=json3&xorb=2&xobt=3&xovt=3"

        self._caption_json = None
        self._events = None
        self._isparseable = True

        self._subtitle = ""
        self._fetchcaption()

        if self._isparseable:
            self._getcaptionlist()

    def _getcaptionlist(self):
        self._events = self._caption_json['events']

    def _fetchcaption(self):
        try:
            self._caption_json = requests.get(self._url).json()
        except ValueError:
            self._isparseable = False

    @staticmethod
    def _showurlerror():
        print("url is expired or not found")

    @abstractmethod
    def _convert(self):
        pass
