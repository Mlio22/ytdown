# get time from ms (json) to srt timing

def mstimetoother(mstime):
    def getroundtime(time, fractor):
        result = time // fractor
        time -= fractor * result

        return time, result

    mstime, hours = getroundtime(mstime, 360000)
    mstime, minutes = getroundtime(mstime, 60000)
    mstime, seconds = getroundtime(mstime, 1000)

    return [str(hours), str(minutes), str(seconds), str(mstime)]

def getsrttime(time):
    [hours, minutes, seconds, mstime] = mstimetoother(time)

    def addzeros(timevar, targetlength):
        while len(timevar) < targetlength:
            timevar = '0' + timevar
        return timevar

    hours = addzeros(hours, 2)
    minutes = addzeros(minutes, 2)
    seconds = addzeros(seconds, 2)
    mstime = addzeros(mstime, 3)

    return "{}:{}:{},{}".format(
            hours, minutes, seconds, mstime
        )


if __name__ == '__main__':
    pass
