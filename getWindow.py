import subprocess
import time
import json 
from airtable import Airtable
from airtableApp import Entry , Tags , aName
from tagTable import TagTbl
from tagTable import SCREEN_LOCKED
import requests

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


'''
class variables
'''
exit = False
at = Airtable(airtableBaseId, airtableAPIKey)
ttbl = TagTbl("DUMMY")
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
        #when the system locks
        return SCREEN_LOCKED
            

pushQueue = []

prevApp = Entry(getRunningProgram()).start()

while not exit:
    currProgram = getRunningProgram()
    
    if currProgram != prevApp.appName:
        prevApp.stop()
        entryDict = prevApp.buildEntry()
        prevApp = Entry(currProgram).start()

        tag = ttbl.lookUp(currProgram)
        if tag is not None:
            prevApp.tags += [tag]
        print(entryDict)

        #update air table
        try:
            at.create(loggerTableName, entryDict)
            print('pushed' , entryDict[aName])

            #if the previous create entry is sucessful then push all the queued
            while pushQueue != []:
                entryDict = pushQueue.pop()
                at.create(loggerTableName, entryDict)
                print('pushed' , entryDict[aName])

        except requests.exceptions.ConnectionError as e:
            pushQueue.append(entryDict)
            print('queued ', len(pushQueue) , " items" , entryDict)


    #wait 10 seconds
    time.sleep(3)

