class Query:
    def __init__(self, user, queryfunction=None, properties=None, startfunction=None):
        self._user = user
        self._query_function = queryfunction
        self._properties = properties
        self._threads = []

        self._iscancelled = False

        self._properties['query_list'].addquery(self)

        self._start_function = startfunction
        self._start_function(self)

    def getuser(self):
        return self._user

    def runqueryfunction(self):
        self._query_function(self)

    def getproperties(self):
        return self._properties

    def setproperty(self, index, data):
        self._properties[index] = data

    def setqueryfunction(self, function):
        self._query_function = function

    def addthread(self, thread):
        self._threads.append(thread)

    def iscancelled(self):
        print(self._iscancelled)
        return self._iscancelled

    def cancelthreads(self):
        self._iscancelled = True
        for thread in self._threads:
            try:
                thread.join()
                print("thread terminated")
            finally:
                None


class Queries:
    def __init__(self):
        self._queries = []

    def checkquery(self, query):
        return query in self._queries

    def addquery(self, query):
        self._queries.append(query)

    def deletequery(self, query):
        print('query deleted0')
        query.cancelthreads()
        print('query deleted1')
        self._queries.remove(query)
        print("query deleted")

    def checkuserquery(self, message):
        for query in self._queries:
            if message.author == query.getuser():
                return query
        return False
