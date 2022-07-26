import json 
import os
from pathlib import Path
class Preferences():

    def __init__(self,path) -> None:
        self.filename = path + "/config.json"
        self.settings_object = dict()
        if not os.path.exists(self.filename):
             self.createPrefFile()
        else:
            self.loadPrefFile()
    
    def loadPrefFile(self):
        with open(self.filename, 'r') as file:
            self.settings_object = json.load(file)

    def createPrefFile(self):
        with open(self.filename,'w') as file:
            self.settings_object = {
                'ar':'',
            }
            file.write(json.dumps(self.settings_object,indent=4))

    def updatePrefFile(self):
        with open(self.filename,'w') as file:
            file.truncate(0)
            file.write(json.dumps(self.settings_object,indent=4)) 

    def put(self,key,value):
        self.settings_object[key]=value
        self.updatePrefFile()


    def get(self,key):
        self.loadPrefFile()
        return self.settings_object[key]

    def getJson(self):
        return self.settings_object

    def checkIfArKeyExists(self):
        return self.get('ar')

    def getConfigFile(self):
        return Path(self.filename)

