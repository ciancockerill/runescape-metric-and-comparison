class PlayerData:
    skillDictionary = {
        0: "Attack",
        1: "Defence",
        2: "Strength",
        3: "Constitution",
        4: "Ranged",
        5: "Prayer",
        6: "Magic",
        7: "Cooking",
        8: "Woodcutting",
        9: "Fletching",
        10: "Fishing",
        11: "Firemaking",
        12: "Crafting",
        13: "Smithing",
        14: "Mining",
        15: "Herblore",
        16: "Agility",
        17: "Thieving",
        18: "Slayer",
        19: "Farming",
        20: "Runecrafting",
        21: "Hunter",
        22: "Construction",
        23: "Summoning",
        24: "Dungeoneering",
        25: "Divination",
        26: "Invention",
        27: "Archaeology",
        28: "Necromancy",
    }

    def __init__(self, apiData):
        self.apiData = apiData
        self.formattedPlayerData = None

        if apiData is not None:
            self.formattedPlayerData = {
                "name": apiData["name"],
                "totalskill": apiData["totalskill"],
                "totalxp": apiData["totalxp"],
                "completedquests": apiData["questscomplete"]
            }

            self.__formatSkills()

    def __formatSkills(self):
        skillsList = []

        for skill in self.apiData["skillvalues"]:
            tempList = [self.skillDictionary[skill["id"]], skill["level"]]
            skillsList.append(tempList)

        self.formattedPlayerData["skills"] = skillsList

    def getFormattedData(self):
        return self.formattedPlayerData

    def printFormattedData(self):
        for k, v in self.formattedPlayerData.items():
            if k != "skills":
                print(k + ":\n\t" + str(v))
            else:
                print("Skills:")

                for skills in self.formattedPlayerData["skills"]:
                    print("\t" + str(skills))