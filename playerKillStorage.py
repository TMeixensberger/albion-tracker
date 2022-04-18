import os
import tempfile
import json
from os.path import exists

from killApi import KillApi


class PlayerKillStorage():

    def __init__(self, playerName) -> None:
        self.__playerName = playerName
        self.__storageFile = "{0}/kills-{1}.json".format(
            tempfile.gettempdir(), playerName)

    def load(self):
        if os.path.exists(self.__storageFile):
            f = open(self.__storageFile, "r+")
            data = json.load(f)
            f.close()
            return data
        else:
            return {}

    def save(self, data):
        jsonData = json.dumps(data)
        f = open(self.__storageFile, "w+")
        f.write(jsonData)
        f.close()

    def refresh(self):
        ret, apiKills = KillApi().getByName(self.__playerName)
        if ret:
            data = self.load()
            for apiKill in apiKills:
                if str(apiKill["EventId"]) not in data:
                    data[str(apiKill["EventId"])] = {
                        "posted": False, "data": apiKill}
            self.save(data)

    def unpostedKillsAvailable(self):
        found = False
        data = self.load()
        for id in data:
            kill = data[id]
            if kill["posted"] == False:
                found = True
        return found

    def getUnpostedKills(self):
        data = self.load()
        kills = {}
        for id in data:
            kill = data[id]
            if kill["posted"] == False:
                kills[id] = kill
                data[id]["posted"] = True
        self.save(data)
        return kills
