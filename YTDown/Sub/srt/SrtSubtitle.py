from YTDown.Sub.parser import Subtitle
from YTDown.Sub import utils as commonutils
from operator import itemgetter


class SrtSubtitle(Subtitle):
    def __init__(self, url):
        super().__init__(url)
        if self._isparseable:
            self._convert()
        else:
            self._showurlerror()

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
