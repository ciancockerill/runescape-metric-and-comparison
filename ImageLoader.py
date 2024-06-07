import os

import requests
import aiohttp
from requests import RequestException

import playerData


class ImageLoader:
    def __init__(self):
        self.wikiImageURL = "https://runescape.wiki/images/"
        self.localDir = "images/skills/"
        self.directoryTable = {}
        self.skillNames = playerData.PlayerData.skillDictionary.values()
        self.__downloadSkillImages()

    def __DoesImageExist(self, skill, imgData):
        localImageDir = self.localDir + skill + ".png"

        if not os.path.exists(localImageDir):
            return False

        existingFile = open(localImageDir, "rb").read()

        return existingFile == imgData

    def __downloadSkillImages(self):
        if not os.path.exists(self.localDir):
            os.makedirs(self.localDir)
            print("Created new Local Directory: " + self.localDir)

        for skill in self.skillNames:
            imgData = requests.get(self.wikiImageURL + skill + ".png").content

            if self.__DoesImageExist(skill, imgData):
                print("..." + skill + " Image Already Saved")
            else:
                try:
                    handler = open(self.localDir + skill + ".png", "wb")
                    handler.write(imgData)
                    self.directoryTable[skill] = (self.localDir + skill + ".png")
                    print("...Loaded " + skill + " Image")
                except RequestException as exception:
                    raise RuntimeError(f"Failed to download image for skill '{skill}': {exception}")
                except IOError as exception:
                    raise RuntimeError(f"Failed to save image for skill '{skill}' to local directory: {exception}")

            self.directoryTable[skill] = (self.localDir + skill + ".png")

    def getImageDirectories(self):
        return self.directoryTable
