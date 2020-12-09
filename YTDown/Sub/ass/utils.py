from math import floor, pow

# video_size that used in this project
VIDEO_SIZE = [384, 288]


def checknull(raw, attr, defvalue):
    """
    check if the value of object's property is exist or not.
    if null return defvalue
    if not, return the value

    :param raw: the object (dict)
    :param attr: attribute of the dict (string)
    :param defvalue: default value (alltype)
    :return: the value or the default
    """
    try:
        return raw[attr]
    except:
        return defvalue


def writeevent(pens, wps, wss, segs, time, penid, wpid, wsid, karaokes, isdefault):
    [start, end] = settime(time['t'], time['d'])

    seg_items = []
    karaoke_child_iter = 0

    for seg in segs:
        new_word = ""
        for i in range(len(seg['utf8'])):
            new_word += "\\N" if ord(seg['utf8'][i]) == 10 else seg['utf8'][i]

        seg_items.append({
            'text': new_word,
            'p': checknull(seg, 'pPenId', penid),
            'wp': wpid,
            'ws': wsid,
            't0': checknull(karaokes, karaoke_child_iter, False)
        })

        karaoke_child_iter += 1

    tagged_seg = ""
    style = ""


    for seg_child in seg_items:
        if isdefault:
            tagged_seg += seg_child['text']
            style = "Youtube Default"
        else:
            tagged_seg += addtag(seg_child, pens[seg_child['p']], wps[seg_child['wp']], wss[seg_child['ws']])
            is_opaque = pens[seg_child['p']]['bo'] != 0

            style = "Default Opaque" if is_opaque else "Default"


    [layer, name, marginL, marginR, marginV, effect] = [0, "", 0, 0, 0, ""]
    return "Dialogue: {},{},{},{},{},{},{},{},{},{}\n".format(
        layer, start, end, style, name, marginL, marginR, marginV, effect, tagged_seg
    )


# time utils
def converttime(time):

    """
    :param time: miliseconds(int):
    :return: time with string format (hh:mm:ss.time)
    """

    [h, m, s] = [0, 0, 0]

    if time / 60000 >= 60:
        h = time // 360000
        time -= h * 360000

    if time / 1000 >= 60:
        m = time // 60000
        time -= m * 60000

    if time / 1000 >= 1:
        s = time // 1000
        time -= s * 1000

    #  jika sisa milisecond kurang dari 3 digit maka harus ditambah 0 dari depan
    #  dan akan diambil 2 digit terdepan
    #  dan diubah menjadi string

    if time < 100:
        # mengubah menjadi string
        time = "0" + str(time)
    time = str(time)

    time = time[0:2]

    #  jika jumlah menit dan detik kurang dari 2 digit maka harus ditambah 0 dari depan
    if m < 10:
        # mengubah menjadi string
        m = "0" + str(m)

    if s < 10:
        # mengubah menjadi string
        s = "0" + str(s)

    return "{}:{}:{}.{}".format(h, m, s, time)


def settime(start, duration):
    return [converttime(start), converttime(start + duration)]


# styled utilities
def getfontsize(fs):
    """
    return from youtube font size to aegisub (proper) font size
    youtube default is 100, aegisub default 15 (defined by myself)
    the formula is easier to explain in the algorithm below

    :param fs: font size (youtube) (int)
    :return: font size (aegisub) (float / int)
    """

    if fs == 100:
        return 15
    elif fs < 100 and fs != 1:
        return 15 - floor((100 - fs) / 26.5)
    elif fs > 100:
        return 15 + floor((fs - 100) / 26.5)
    elif fs == 1:
        # minimum font size for aegisub is 10
        return 10


def getfonttype(fn):
    """
    youtube only supports this following fonts:
    1: Courier New
    2: Times New Roman
    3: DejaVu Sans Mono
    4: Roboto
    5: Comic Sans Ms
    6: Monotype Corsiva
    7: Carrois Gothic SC

    :param fn: font number from youtube (int)
    :return: font type in aegisub (string)
    """

    FONTS = [
        "Courier New",
        "Times New Roman",
        "DejaVu Sans Mono",
        "Roboto",
        "Comic Sans Ms",
        "Monotype Corsiva",
        "Carrois Gothic SC"
    ]

    if fn < 8:
        return FONTS[fn-1]
    else:
        return FONTS[3]


def setcolor(deccolor, maxpow):
    """
    Convert from DEC Color to HEX Color
    and convert it again from HEX to ASS

    forecolor and backcolor use 6 digit HEX
    foreopacity and backopacity use 3 digit HEX

    :param deccolor: DEC Color number (int)
    :param maxpow: HEX Length max
    :return: ASS Color (string), ex &H[ass_color]&
    """
    # change from DEC Color to HEX Color first

    # for 6 digit HEX we can directly use hex() function
    hex_color = ""
    for i in range(maxpow, -1, -1):
        hex_number = int(pow(16, i))
        if deccolor >= hex_number:
            result = floor(deccolor / hex_number)
            hex_color += str(format(result, 'x'))
            deccolor -= result * hex_number
        else:
            hex_color += '0'

    """
    change from HEX Color to ASS Color
    HEX color -> ASS color
    HEX (ABCDEF) -> ASS (EFCDAB)
    """

    ass_color = hex_color[4:6] + hex_color[2:4] + hex_color[0:2]
    return "&H" + ass_color.upper() + "&"


def getalign(ap):
    """
    returns align point from youtube to aegisub
    align point(ap) in youtube:
    
    0       1       2

    3       4       5

    6       7       8

    align point in aegisub:

    7       8       9
    
    4       5       6

    1       2       3
    
    :param ap: align point (youtube) (int) 
    :return: align point (aegisub) (int)
    """

    if ap < 3:
        return ap + 7
    elif ap < 6:
        return ap + 1
    elif ap < 9:
        return ap - 5


def getpos(total, percentage):
    """
    returns the precise location of subtitle in the video (in px)
    total is usually from VIDEO_SIZE
    :param total: (int)
    :param percentage: (int)
    :return: the location of text in pixel (float)
    """
    return (total * percentage) / 100


def addtag(seg, pen, wp, ws):
    """
    :param seg:
    :param pen:
    :param wp:
    :param ws:
    :return:
    """

    start_tags = ""
    end_tags = ""

    # font bold/italic/underline
    if pen['b']:
        start_tags += "\\b1"
        end_tags += "\\b0"

    if pen['i']:
        start_tags += "\\i1"
        end_tags += "\\i0"

    if pen['u']:
        start_tags += "\\u1"
        end_tags += "\\u0"

    # font property
    if pen['fs'] != 100:
        start_tags += "\\fs{}".format(getfontsize(pen['fs']))

    if pen['fn'] != 4:
        start_tags += "\\fn{}".format(getfonttype(pen['fn']))

    # font forecolor
    if pen['fc'] != 16777215:
        start_tags += "\\c{}".format(setcolor(pen['fc'], 5))

    if pen['fo'] != 254:
        start_tags += "\\1a{}".format(setcolor(abs(pen['fo'] - 254), 1))

    # font backcolor
    if pen['bc'] != 0:
        start_tags += "\\3c{}".format(setcolor(pen['bc'], 5))

    if pen['bo'] != 0:
        start_tags += "\\3a{}".format(setcolor(abs(pen['bo'] - 254), 1))
    elif pen['bo'] == 0:
        start_tags += "\\3a&H65&"


    # font positions
    al = getalign(wp['ap'])
    [posx, posy] = [getpos(VIDEO_SIZE[0], wp['ah']), getpos(VIDEO_SIZE[1], wp['av'])]

    start_tags += "\\an{}\\pos({},{})".format(al, posx, posy)

    # karaoke text (if any)
    # t0 = str(seg['t0'])
    # if t0:
    #     t0 = t0[0:(len(t0) - 1)]
    #     start_tags += "\\k{}".format(t0)

    if start_tags != "":
        start_tags = '{' + start_tags + '}'

    if end_tags != "":
        end_tags = '{' + end_tags + '}'

    return start_tags + seg['text'] + end_tags


# debug
if __name__ == "__main__":
    # getpos(288, 100)
    # print(setcolor(526344, 5))
    pass