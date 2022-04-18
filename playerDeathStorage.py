import os
import tempfile
import json
from os.path import exists

from deathApi import DeathApi


class PlayerDeathStorage():

    def __init__(self, playerName) -> None:
        self.__playerName = playerName
        self.__storageFile = "{0}/deaths-{1}.json".format(
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
        ret, apiDeaths = DeathApi().getByName(self.__playerName)
        if ret:
            data = self.load()
            for apiDeath in apiDeaths:
                if str(apiDeath["EventId"]) not in data:
                    data[str(apiDeath["EventId"])] = {
                        "posted": False, "data": apiDeath}
                    print("Death added")
            self.save(data)

    def unpostedDeathsAvailable(self):
        found = False
        data = self.load()
        for id in data:
            death = data[id]
            if death["posted"] == False:
                found = True
        return found

    def getUnpostedDeaths(self):
        data = self.load()
        deaths = {}
        for id in data:
            death = data[id]
            if death["posted"] == False:
                deaths[id] = death
                data[id]["posted"] = True
        self.save(data)
        return deaths


#o = PlayerDeathStorage("MixiHD")
# o.refresh()
# print(len(o.getUnpostedDeaths()))
