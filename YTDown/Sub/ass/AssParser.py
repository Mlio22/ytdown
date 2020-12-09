import abc
from .utils import checknull


class AssParser(metaclass=abc.ABCMeta):
    def __init__(self, raw):
        self._raw = raw
        self._properties = []

        if isinstance(self._raw, list):
            if len(self._raw) > 1:
                for raw in self._raw:
                    self._properties.append(self._parseproperties(raw))

    @property
    def properties(self):
        return self._properties

    @abc.abstractmethod
    def _parseproperties(self, raw):
        pass


class PenParser(AssParser):
    def _parseproperties(self, raw):
        return {
            # todo: offset is still not explored yet!
            'of': checknull(raw, 'ofOffset', 2),

            # get pen font style properties
            'b': checknull(raw, 'bAttr', 0),  # bold (0/1)
            'i': checknull(raw, 'iAttr', 0),  # italic (0/1)
            'u': checknull(raw, 'uAttr', 0),  # underline (0/1)
            'fs': checknull(raw, 'szPenSize', 100),  # font size
            'fn': checknull(raw, 'fsFontStyle', 4),  # font style (font type)


            # get pen font color
            # warna teks youtube menggunakan warna decimal
            # sedangkan aegisub menggunakan warna ASS
            #
            # Youtube DEC Color => HEX Color
            # (0 - 16777215)    => (000000 - FFFFFF)
            #
            # dari HEX Color ini akan diubah jadi ASS Color
            # HEX Color     => ASS Color
            # (ABCDEF)      => (EFCDAB)
            #
            # silahkan cek Utils/setcolor() untuk lebih lanjut

            'fc': checknull(raw, 'fcForeColor', 16777215),  # foreground color
            'bc': checknull(raw, 'bcBackColor', 526344),  # background color

            #
            # opacity text pada youtube berkebalikan dengan aegisub
            # jika youtube dari 0 (transparan) => 255 (jelas)
            # maka aegisub dari 255 (transparan) => 0 (jelas)
            #
            
            'fo': checknull(raw, 'foForeAlpha', 255),
            'bo': checknull(raw, 'boBackAlpha', 0)

            # todo: et(edgeType) dan ec(edgeColor) belum ditentukan
        }


class WSParser(AssParser):
    def _parseproperties(self, raw):
        """
        justifies(ju) pada youtube:

        1(left)       2(center)       3(right)

        namun dalam praktik, ju ini jarang digunakan selain yang bernilai 2
        """

        return {
            'align': {
                'ju': checknull(raw, 'juJustifCode', 2)
            },
            'vertical': {
                # todo: aegisub's macro (pd and sd) still not been explored yet
                'pd': checknull(raw, 'pdPrintDir', 0),
                'sd': checknull(raw, 'dfScrollDir', 0)
            }
        }


class WPParser(AssParser):
    def _parseproperties(self, raw):
        return {
            'ap': checknull(raw, 'apPoint', 7),
            'ah': checknull(raw, 'ahHorPos', 50),
            'av': checknull(raw, 'avVerPos', 95)
        }


class EventParser(AssParser):
    def _parseproperties(self, raw):
        return {
            'time': {
                't': checknull(raw, 'tStartMs', 0),
                'd': checknull(raw, 'dDurationMs', 0)
            },
            'segs': checknull(raw, 'segs', []),
            'win': {
                'wp': checknull(raw, 'wpWinPosId', 0),
                'ws': checknull(raw, 'wsWinStyleId', 0)
            },
            'p': checknull(raw, 'pPenId', 0)
        }

