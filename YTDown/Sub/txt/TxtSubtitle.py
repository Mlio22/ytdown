from YTDown.Sub.parser import Subtitle


class TxtSubtitle(Subtitle):
    def __init__(self, url):
        super().__init__(url)
        if self._isparseable:
            self._convert()
            self._showsubtitle()
        else:
            self._showurlerror()

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

