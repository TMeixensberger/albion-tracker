import requests
from playerApi import PlayerApi


class DeathApi():

    def getByName(self, playerName):
        if PlayerApi().existsByName(playerName):
            playerId = PlayerApi().convertName2Id(playerName)
            ret, data = self.getById(playerId[1])
            return ret, data
        else:
            return False, {}

    def getById(self, playerId):
        if PlayerApi().existsById(playerId):
            url = "https://gameinfo.albiononline.com/api/gameinfo/players/{0}/deaths".format(
                playerId)
            req = requests.get(url)
            if req.status_code == 200:
                jsonData = req.json()
                return True, jsonData
        else:
            return False, {}
