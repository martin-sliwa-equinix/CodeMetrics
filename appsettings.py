from pathlib import Path
import jsonpickle
import os

class Config:
    def __init__(self):
        #Set defaults
        self.updatefreq = 60
        self.filename = "settings.txt"
        self.trackedrepos = {}
        self.trackedusers = {}
        self.load_settings()

    def load_settings(self):
        settingspath = Path("./"+self.filename)
        if settingspath.exists():

            settingsdata = open(settingspath).read()
            self = jsonpickle.decode(settingsdata)
        else:
            print("Settings file does not exist. Creating file.")
            self.create_settings()

    def create_settings(self):
        jsondata = jsonpickle.encode(self)
        with open(self.filename, "w") as sf:
            sf.write(jsondata)

    def update_settings(self):
        print("Todo")

    def delete_settings(self, path):
        os.remove(path)