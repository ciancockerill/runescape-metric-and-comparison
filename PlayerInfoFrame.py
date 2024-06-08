import tkinter as tk
from PIL import ImageTk, Image

import MainApplication

__baseFont = "Verdana"
LARGE_FONT_BOLD = (__baseFont, 20, "bold")
LARGE_FONT = (__baseFont, 12)
SKILL_FONT = (__baseFont, 10, "bold")
SMALL_FONT = (__baseFont, 8)

IMAGE_SIZE = 25

ERROR_MESSAGE = "Profile Doesn't Exist or Profile is Private"

MAX_SKILLS_PER_ROW = 4

class PlayerInfo(tk.Frame):
    def __init__(self, parent, playerData):
        super().__init__(parent, bg=MainApplication.MODULE_COLOR)
        self.bgColor = MainApplication.BACKGROUND_COLOR
        self.textColor = "white"

        self.nameLabel = None
        self.totalxpLabel = None
        self.totalSkillLabel = None
        self.totalQuestsLabel = None
        self.errorLabel = None

        self.playerData = playerData

        self.update_idletasks()
        self.config(height=parent.winfo_height(), width=parent.winfo_width())
        self.pack_propagate(True)

        if playerData is not None:
            self.showPlayerInfo()
        else:
            self.showError()

    def showError(self):
        self.errorLabel = tk.Label(self, text=ERROR_MESSAGE, font=LARGE_FONT)
        self.errorLabel.grid(row=0, column=1, columnspan=2, pady=10)

    def showPlayerInfo(self):
        self.nameLabel = tk.Label(self, text=self.playerData["name"], font=LARGE_FONT_BOLD, bg=self.bgColor, fg=self.textColor)
        self.nameLabel.grid(row=0, column=1, columnspan=2, pady=10)

        self.totalxpLabel = tk.Label(self, text="Total XP: " + str(self.playerData["totalxp"]), font=LARGE_FONT, bg=self.bgColor, fg=self.textColor)
        self.totalxpLabel.grid(row=1, column=1, columnspan=2, pady=10)

        self.totalSkillLabel = tk.Label(self, text="Total Level: " + str(self.playerData["totalskill"]),
                                        font=LARGE_FONT, bg=self.bgColor, fg=self.textColor)
        self.totalSkillLabel.grid(row=2, column=1, columnspan=2, pady=10)

        self.totalQuestsLabel = tk.Label(self, text="Quests Completed: " + str(self.playerData["completedquests"]),
                                         font=LARGE_FONT, bg=self.bgColor, fg=self.textColor)
        self.totalQuestsLabel.grid(row=3, column=1, columnspan=2, pady=10)

        # Track row and column indices for skill labels
        row_index = 4
        column_index = 0

        for skills in self.playerData["skills"]:
            skill_name = skills[0]
            skill_value = str(skills[1])

            # Create and place skill label
            skillLabel = SkillFrame(self, skill_name, skill_value)
            skillLabel.grid(row=row_index, column=column_index, pady=5, padx=5)

            # Increment row and column indices
            column_index += 1
            if column_index >= MAX_SKILLS_PER_ROW:
                column_index = 0
                row_index += 1

class SkillFrame(tk.Frame):
    def __init__(self, parent, skillName, skillValue):
        super().__init__(parent)
        self.panel = None
        self.image = None
        self.parent = parent

        self.skillName = skillName
        self.skillDirectory = MainApplication.MainApplication.skillImageDirectories[skillName]
        self.skillValue = skillValue
        self.pack_propagate(True)

        self.buildPanel()

    def getImage(self):
        img = Image.open(self.skillDirectory)
        img = img.resize((25, 25))
        self.image = ImageTk.PhotoImage(img)
        return self.image

    def buildPanel(self):
        self.image = self.getImage()
        # Create a Label with both text and image
        self.panel = tk.Label(self, text=self.skillValue, image=self.image, compound="right", font=SKILL_FONT, padx=7)
        self.panel.config(bg=MainApplication.BACKGROUND_COLOR, fg="white")
        self.panel.grid()
