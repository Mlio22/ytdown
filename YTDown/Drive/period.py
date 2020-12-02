from datetime import datetime, timedelta
from YTDown.Drive.db.db import parsesavedfile, db_file
from YTDown.Drive.utils import deletebyid
from threading import Timer


class Period:
    def __init__(self, fileid, deadline, periodlist):
        self._fileid = fileid
        self._deadline = deadline
        self._period_list = periodlist

        self._settimer()

    def _settimer(self):
        def deletedfilecallback():
            deletebyid(self._fileid)
            print("file deleted")
            self._period_list.removeperiod(self)
            print("period exterminated")

        time_now = datetime.now()
        if isinstance(self._deadline, str):
            delta = (datetime.strptime(self._deadline, "%Y-%m-%d %H:%M:%S.%f") - time_now).total_seconds()
        else:
            delta = (self._deadline - time_now).total_seconds()

        timer = Timer(delta, deletedfilecallback)
        timer.start()

    def getfileid(self):
        return self._fileid


class PeriodList:
    def __init__(self):
        self._db_file = db_file
        self._parsedsavedfiles = parsesavedfile()

        self._periods = []

        for parsedfile in self._parsedsavedfiles:
            self._periods.append(Period(parsedfile['fileid'], parsedfile['deadline'], self))

    def addperiod(self, fileid):
        deadline = datetime.now() + timedelta(minutes=1)
        self._periods.append(Period(fileid, deadline, self))
        print("added period", fileid)

        self._addtodb(fileid, deadline)

    def removeperiod(self, period):
        self._removefromdb(period.getfileid())
        self._periods.remove(period)

    def _addtodb(self, fileid, deadline):
        print("start adding to db")
        self._parsedsavedfiles.append({
            'fileid': fileid,
            'deadline': deadline
        })

        print("added to db", fileid)
        self._rewritedbfile()

    def _removefromdb(self, fileid):
        for parsedfile in self._parsedsavedfiles:
            if parsedfile['fileid'] == fileid:
                self._parsedsavedfiles.remove(parsedfile)

        self._rewritedbfile()

    def _rewritedbfile(self):
        print("start to updating file")
        file_content = ""
        for index, parsedfile in enumerate(self._parsedsavedfiles):
            if index > 0:
                file_content += "\n"

            file_content += "{}|{}".format(parsedfile['fileid'], parsedfile['deadline'])
            print(file_content)

        self._db_file.SetContentString(file_content)
        self._db_file.Upload()

        print("file updated")

