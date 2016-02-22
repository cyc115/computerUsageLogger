import subprocess
import time
import json 
from airtable import Airtable
from airtableApp import Entry

#TODO read the list of tag and associated window name from a predefined persistent file
#TODO make an interface to toggle time tracking
#TODO make an interface to allow adding tag
#TODO detect mouse inactivity to stop/resume tracking when necessary

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

'''
class methods
'''
def getRunningProgram () :
    output_byte = subprocess.check_output(cmd, shell=True)
    return output_byte.decode('utf-8')[0:-1]


prevApp = Entry(getRunningProgram()).start()

print('current program ' , prevApp.appName)

while not exit:
    currProgram = getRunningProgram()
    if currProgram != prevApp.appName:
        prevApp.stop()
        entryDict = prevApp.buildEntry()
        prevApp = Entry(currProgram).start()

        print('changed to ' , prevApp.appName, " update airtable")
        #update air table
        at.create(loggerTableName, entryDict)

        print ('backend updated!')

    #wait 10 seconds
    time.sleep(3)

