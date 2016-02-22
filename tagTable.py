from airtableApp import Tags

'''
a list of default apps that can be tagged
'''
SCREEN_LOCKED = 'screen locked'
CHROME = 'chrome'

tags = {}
class TagTbl():
    def __init__(self,dir):
        tags[SCREEN_LOCKED] = Tags.IDLE
        tags[CHROME] = Tags.WEB
        tags['java'] = Tags.PROGRAMMING
        tags['zeal'] = Tags.PROGRAMMING
        tags['skype'] = Tags.COMMUNICATION
        tags['gnome-terminal'] = Tags.PROGRAMMING
        tags['gnome-system-mo'] = Tags.IDLE
        tags['steam'] = Tags.ENTERTAINMENT
        tags['dontstarve_steam'] = Tags.ENTERTAINMENT
        return
        
    def lookUp(self,appName=""):
        return tags.get(appName)
    
