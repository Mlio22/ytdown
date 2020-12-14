from datetime import datetime
from YTDown.Drive.db.db import savedpreviousfiles, db_file
from YTDown.Drive.drive import deletebyid, deletebyname
from threading import Timer
from abc import abstractmethod
from YTDown.conf import LOCAL_CACHE_DELETION_MINUTES, GD_CACHE_DELETION_MINUTES

"""
There are two main subjects in this file:
Period and PeriodList that will be describes in each class
"""


class Period:
    def __init__(self, periodlist, default_cache_minutes, timestamp):
        """
        Period is a class that sets a timer to delete files periodically
        the subclasses are:
            GDPeriod for deleting Google drive files
            LocalPeriod for local caches

        go to YTDown/conf.py to set:
            LOCAL_CACHE_DELETION_MINUTES    : timeout for local caches (in minutes)
            GD_CACHE_DELETION_MINUTES       : timeout for GD files (in minutes)
        """

        """    
        :param periodlist: 
        :param default_cache_minutes: timeout for this period (in minutes)
        :param timestamp: 
        """
        self._period_list = periodlist
        self.__timestamp = timestamp

        self.__deltatime = 0
        self._default_cache_time_minutes = default_cache_minutes

        self.__setdelta()
        self.__settimer()

    def __setdelta(self):
        """
        todo: perbaiki masalah waktu mundur yang tiba-tiba negatif

        sets timer's timeout
        :return: None
        """
        time_now = datetime.now()

        if self.__timestamp != '':
            self.__deltatime = (self.__timestamp - time_now).total_seconds()

        if self.__timestamp is None or self.__deltatime < 0:
            self.__deltatime = self._default_cache_time_minutes * 60

    def __settimer(self):
        """
        run the timer and run the callback when the time's out

        note: timer should not be stopped
        :return: None
        """
        print("timer started")
        print("time left: ", self.__deltatime, "seconds")
        Timer(self.__deltatime, self._timercallback).start()

    @abstractmethod
    def _timercallback(self):
        """
        run the callback function
        :return:
        """
        pass


class GDPeriod(Period):
    def __init__(self, periodlist, fileid, timestamp):
        self.__fileid = fileid
        super().__init__(periodlist, GD_CACHE_DELETION_MINUTES, timestamp)

    def _timercallback(self):
        self._period_list.removeperiod(self, fileid=self.__fileid)


class LocalPeriod(Period):
    def __init__(self, periodlist, filename, timestamp):
        self.__filename = filename
        super().__init__(periodlist, LOCAL_CACHE_DELETION_MINUTES, timestamp)

    def _timercallback(self):
        self._period_list.removeperiod(self, filename=self.__filename)


class PeriodList:
    def __init__(self):
        """
        Periodlist is a class to contain list of Periods
        that should be able to be added, and remove

        PeriodList managed to control the periods,
        delete local caches and GD files,
        and rewrite the database file that stored in GD
        """

        self._periods = []
        self._db_file = db_file

        # gets previous saved files whose not deleted before
        # and saves the upcoming new period
        self._parsedsavedfiles = savedpreviousfiles()

        # set periods to previous files
        self.__setprevioustimer()

    def __setprevioustimer(self):
        for parsedfile in self._parsedsavedfiles:
            print(parsedfile)
            self.__addperiod(
                parsedfile['fileid'],
                parsedfile['filename'],
                parsedfile['timestampgd'],
                parsedfile['timestamplocal']
            )

    def __addperiod(self, fileid, filename, timestampgd, timestamplocal):
        """
        the inner function
        sets the GDperiod and LocalPeriod strictly

        :param fileid: the id of GD file (str)
        :param filename: the name of file (str)
        :param timestampgd: the previous timestamp for the GD file (str)
        :param timestamplocal: the previous timestamp for the local cache (str)
        :return: None
        """
        self._periods.append(GDPeriod(self, fileid, timestampgd))
        self._periods.append(LocalPeriod(self, filename, timestamplocal))

    def addnewperiod(self, filetype, fileid, filename, timestampgd=datetime.now(), timestamplocal=datetime.now()):
        """
        usually called in video or sub function to create new period using the inner __addperiod

        :param filetype: the type of the file, used to help the seaching for saved cache
        the other params is same as function above

        :return: None
        """
        print("creating period")

        # set to only file's name and format
        filename = filename.replace(
            "C:\\Users\\Acer\\Documents\\TELKOM TUGAS\\python_dev\\ytdown-dc-bot\\YTDown\\Bot\\../cache/video/",
            ""
        )

        # rewriting the db file
        self.__addtodbfile(filetype, fileid, filename, timestampgd, timestamplocal)
        # creating 2 periods for a file
        self.__addperiod(fileid, filename, timestampgd, timestamplocal)

    def __addtodbfile(self, filetype, fileid, filename, timestampgd, timestamplocal):
        """
        adds a period to periodlist and rewrites the db file
        """
        print("start adding to db file")
        self._parsedsavedfiles.append({
            'filetype': filetype,
            'fileid': fileid,
            'filename': filename,
            'timestampgd': timestampgd,
            'timestamplocal': timestamplocal
        })

        self.__rewritedbfile()

    def removeperiod(self, period, fileid=None, filename=None):
        """
        removes a period from periodlist and rewrites the db file
        :return:
        """
        # checks is period in list
        for parsedfile in self._parsedsavedfiles:
            if parsedfile['fileid'] == fileid:
                parsedfile['timestampgd'] = None
                deletebyid(fileid)
                print("gd file removed")
            elif parsedfile['filename'] == filename:
                parsedfile['timestamplocal'] = None
                deletebyname(parsedfile['filetype'], filename)
                print("local file deleted")

            if parsedfile['timestampgd'] is None and parsedfile['timestamplocal'] is None:
                print("file deleted")
                self._parsedsavedfiles.remove(parsedfile)

        try:
            self._periods.remove(period)
        finally:
            pass

        self.__rewritedbfile()

    def __rewritedbfile(self):
        """
        rewrites the db file

        the db file format is just like this:
        filetype|fileid|filename|timestamp for GD|timestamp for local
        """

        print("start to updating db file")

        file_content = ""
        for index, parsedfile in enumerate(self._parsedsavedfiles):
            print(parsedfile)
            if index > 0:
                file_content += "\n"

            gdtime, localtime = None, None
            if parsedfile['timestampgd']:
                gdtime = parsedfile['timestampgd'].strftime("%d %m %y %H:%M:%S")

            if parsedfile['timestamplocal']:
                localtime = parsedfile['timestamplocal'].strftime("%d %m %y %H:%M:%S")

            file_content += "{}|{}|{}|{}|{}".format(
                parsedfile['filetype'],
                parsedfile['fileid'],
                parsedfile['filename'],
                gdtime,
                localtime
            )

        # sets the GD database file and reuploads it
        self._db_file.SetContentString(file_content)
        self._db_file.Upload()

        print("file updated")
