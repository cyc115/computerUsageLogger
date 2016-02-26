from airtableApp import Tags

'''
a list of default apps that can be tagged
'''
SCREEN_LOCKED = 'screen locked'

tags = {}
class TagTbl():

    def __init__(self,path):
        '''

        :param path: path of the Tag file
        (TODO not yet implemented)
        '''


        tags[SCREEN_LOCKED] = Tags.IDLE
        tags['chrome'] = Tags.WEB
        tags['java'] = Tags.PROGRAMMING
        tags['zeal'] = Tags.PROGRAMMING
        tags['skype'] = Tags.COMMUNICATION
        tags['gnome-terminal'] = Tags.PROGRAMMING
        tags['gnome-system-mo'] = Tags.IDLE
        tags['steam'] = Tags.ENTERTAINMENT
        tags['dontstarve_steam'] = Tags.ENTERTAINMENT

        
    def lookUp(self,appName=""):
        '''
        look up the app name in the tagTable
        :param appName:
        :return:
        '''
        return tags.get(appName)
    
