import subprocess
import time
import json 
from airtable import Airtable
from airtableApp import Entry , Tags , aName
from tagTable import TagTbl
from tagTable import SCREEN_LOCKED
from collections import OrderedDict
import requests
import threading
from tkinter import Tk

#TODO the cmd line has some trouble getting the name of some windows eg. steam, see if it's possible to do so
#TODO read the list of tag and associated window name from a predefined persistent file
#TODO make an interface to toggle time tracking
#TODO make an interface to allow adding tag
#TODO detect mouse inactivity to stop/resume tracking when necessary
#TODO CPU usage is too much and spikes, it's very bad for the battary. I should see if I can combine the push data and push in a lower interval

#const
airtableAPIKey = "keybBQanzhJwdlveV"
airtableBaseId = "appjOjH6SqE5fiIWS"
loggerTableName = 'Application'
cmd = 'cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/comm'
CHECK_INTERVAL = 1;


'''
class variables
'''
exit = False
at = Airtable(airtableBaseId, airtableAPIKey)



'''
window related
'''
root = Tk()

def getMouseLocation():
    '''
    get the latest mouse location
    :return: (x, y) mouse location relative the the screen
    '''
    p = root.winfo_pointerxy()
    return p

'''
class methods
'''
def getRunningProgram () :
    '''
    returns the name of the running program 
    '''
    try:
        output_byte = subprocess.check_output(cmd, shell=True)
        return output_byte.decode('utf-8')[0:-1]
    except subprocess.CalledProcessError :
        print("cannot get process name")
        #when the system locks
        return SCREEN_LOCKED
            
#use pushQueue as a cache for log entries when network is unavailable
pushQueue = []


ttbl = TagTbl("DUMMY/path/to/tag/file")

def updateATble(entryDict : OrderedDict)  -> None:
    '''
    push an entry to airtable
    :param entryDict:
    :return:
    '''
    at.create(loggerTableName, entryDict)
    print('pushed' , entryDict[aName])

    #if the previous create entry is successful then push all the queued
    while pushQueue != []:
        entryDict = pushQueue.pop()
        at.create(loggerTableName, entryDict)
        print('pushed' , entryDict[aName])


prevApp = Entry(getRunningProgram()).startCount()

def checkCurrentApp () -> None:
    global prevApp
    appName = getRunningProgram()

    prevAppName = ""
    if prevApp is not None:
        prevAppName = prevApp.appName
    print('checkCurrentApp')

    if appName != prevAppName:
        prevApp.stopCount()

        #build the previous entry
        logEntry = prevApp.buildLogEntry()

        #start the next log
        prevApp = Entry(appName).startCount()

        #add tags to the new log entry
        tag = ttbl.lookUp(appName)
        if tag is not None:
            prevApp.tags += [tag]

        #update air table
        try:
            updateATble(logEntry)
        except requests.exceptions.ConnectionError as e:
            #in case of connection problem, cache the log entry
            pushQueue.append(logEntry)
            print('queued ', len(pushQueue) , " items" , logEntry)

    threading.Timer(CHECK_INTERVAL, checkCurrentApp).start()

'''
start the program
'''


threading.Timer(0,checkCurrentApp).start()
print('hi')
root.title('Logger alpha')
root.mainloop()

print('hi2')


