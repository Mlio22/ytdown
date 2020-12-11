from YTDown.Bot.fetchcommand import fetchyoutubevideodata, fetchyoutubesubdata


class Query:
    def __init__(self, user, properties, querytype):
        self.__user = user
        self.__properties = properties
        self.__threads = []
        self.__querytype = querytype

        self.__query_function = None
        self.__iscancelled = False

        self.__is_video_finished = False
        self.__is_sub_finished = False

        self.__addtoquerylist()
        self.dotask()

    def __addtoquerylist(self):
        self.__properties['query_list'].addquery(self)

    def dotask(self):
        if not self.__iscancelled:
            if self.__querytype == 'alls':
                if not self.__is_video_finished:
                    fetchyoutubevideodata(self)
                elif not self.__is_sub_finished:
                    fetchyoutubesubdata(self)
            elif self.__querytype == 'video' and not self.__is_video_finished:
                fetchyoutubevideodata(self)
            elif self.__querytype == 'sub' and not self.__is_sub_finished:
                fetchyoutubesubdata(self)
            else:
                self.__commitsuicide()
        else:
            self.__commitsuicide()

    def getuser(self):
        """
        get the name of user that queried this
        :return: user name (str)
        """
        return self.__user

    def getproperties(self):
        """
        :return: propeties (dict)
        """
        return self.__properties

    def setproperty(self, index, value):
        """
        set the self.__properties with selected index
        :param index: the index of self.__properties
        :param value: the value of that index
        :return: None
        """
        self.__properties[index] = value

    def videofinished(self):
        print("video finished")
        self.__is_video_finished = True
        self.dotask()

    def subfinished(self):
        self.__is_sub_finished = True
        self.dotask()
    """
    query function is a function that wait for user's response
    with a filter that can determine is user responses to such query or just random texting 
    example algorithm:
    1. user sends $video request
    2. system gets video list, and sends it to the channel
    3. system waits for user's response which video is needed to be downloaded
    4. system filters upcoming responses [eg. only 1 to 20 accepted]
    5. if the filter doesn't match, system keep waiting
    6. if the filter does match, system downloads the video and send it to channel or GD 
    """

    def setqueryfunction(self, function):
        """
        set the query function
        :param function:
        :return: None
        """
        self.__query_function = function

    def runqueryfunction(self):
        """
        run the query function
        :return: None
        """
        self.__query_function(self)

    """
    a query has a threads that should be controlled
    if user cancels a query, then the threads in it must be stopped
    """

    def addthread(self, thread):
        self.__threads.append(thread)

    def cancelthreads(self):
        self.__iscancelled = True
        for thread in self.__threads:
            try:
                thread.join()
                print("thread terminated")
            finally:
                pass

    def iscancelled(self):
        return self.__iscancelled

    def __commitsuicide(self):
        self.__properties['query_list'].deletequery(self)


class Queries:
    def __init__(self):
        self._queries = []

    def checkquery(self, query):
        return query in self._queries

    def addquery(self, query):
        self._queries.append(query)

    def deletequery(self, query):
        query.cancelthreads()
        self._queries.remove(query)

    def checkuserquery(self, message):
        for query in self._queries:
            if message.author == query.getuser():
                return query
        return False
