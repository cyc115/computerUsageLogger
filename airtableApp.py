
from datetime import tzinfo, timedelta, datetime
from collections import OrderedDict
import json


sTime = "start time"
eTime = "end time"
tags = "Tag"
aName = "Application name"

class Entry():

    def __init__(self, name='None'):
        self.appName = name
        self.tags = []

    def buildEntry (self) :
        '''
        validate the object attributes and build the dictionary that can be used to
        make the request to the airTable backend
        :return: OrderedDict representation of the object
        '''


        if hasattr(self, 'sTime') and hasattr(self, 'eTime') \
                and hasattr(self, 'tags') and hasattr(self, 'appName') :
            # this can be processed and build into an ordered dict

            d = {}
            d[sTime] = self.sTime.isoformat()
            d[eTime] = self.eTime.isoformat()
            d[aName] = self.appName
            d[tags] = self.tags

            return OrderedDict(d)

    def start(self):

        '''
        start the timer
        :return: self : the Entry object
        '''

        self.sTime = datetime.now()
        return self

    def stop(self):

        '''
        stop the timer
        :return: self : the Entry object
        '''

        self.eTime = datetime.now()
        return self

class Tags () :
    PROGRAMMING = 'programming'
    WEB = 'web'
    ENTERTAINMENT = 'entertainment'
    WRITING = 'writing'
    COMMUNICATION = 'communication'
    IDLE = 'idle'


