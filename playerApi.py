import requests
import json


class PlayerApi():
    def existsByName(self, playerName):
        api = "https://gameinfo.albiononline.com/api/gameinfo/search?q={0}".format(
            playerName)
        req = requests.get(api)
        if req.status_code == 200:
            jsonData = req.json()
            if len(jsonData["players"]) > 0:
                return True
        return False

    def existsById(self, playerId):
        api = "https://gameinfo.albiononline.com/api/gameinfo/players/{0}".format(
            playerId)
        req = requests.get(api)
        if req.status_code == 200:
            return True
        return False

    def convertName2Id(self, playerName):
        api = "https://gameinfo.albiononline.com/api/gameinfo/search?q={0}".format(
            playerName)
        req = requests.get(api)
        if req.status_code == 200:
            jsonData = req.json()
            if len(jsonData["players"]) > 0:
                return True, jsonData["players"][0]["Id"]
        return False, ""


# PlayerApi().existsByName("MixiHD")
# PlayerApi().existsByName("awhgdu")

# print(PlayerApi().existsById("WXPyH_NASlGo1CLojGXFuw"))
# print(PlayerApi().existsById("WXPyH_NASlGo1CLojGXFuw187"))
