import requests

class RequestAPI:
    def __init__(self, name):
        self.playerData = self.__requestPlayerData(name)

    def __requestPlayerData(self, name):
        response = requests.get(
            "https://apps.runescape.com/runemetrics/profile/profile?user=" + name + "&activities=20")

        response = response.json()

        if "error" in response:
            return None

        return response

    def getPlayerData(self):
        return self.playerData
