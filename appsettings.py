from pathlib import Path
import jsonpickle
import os

class Config:
    def __init__(self):
        #Set defaults
        self.updatefreq = 30
        self.filename = "settings.txt"
        self.settingspath = Path("./"+self.filename)
        self.trackedrepos = []
        self.trackedusers = []
        self.load_settings()

    def load_settings(self):
        if self.settingspath.exists():

            settingsdata = open(self.settingspath).read()
            self = jsonpickle.decode(settingsdata)
        else:
            print("Settings file does not exist. Creating file.")
            self.create_settings()

    def create_settings(self):
        jsondata = jsonpickle.encode(self)
        with open(self.filename, "w") as sf:
            sf.write(jsondata)

    def update_settings(self):
        self.delete_settings()
        self.create_settings()

    def delete_settings(self):
        os.remove(self.settingspath)


#todo 1: Write a component in to this class that will sanitize pickled data on load
#todo 2: Flesh out the pickle update function. Probably just delete the settings file and recreate on each update.