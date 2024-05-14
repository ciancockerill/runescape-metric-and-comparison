import tkinter as tk

import MainApplication

__baseFont = "Verdana"
LARGE_FONT_BOLD = (__baseFont, 12, "bold")
LARGE_FONT = (__baseFont, 12)
SMALL_FONT = (__baseFont, 8)

ERROR_MESSAGE = "Profile Doesn't Exist or Profile is Private"


class PlayerInfo(tk.Frame):
    def __init__(self, parent, playerData):
        super().__init__(parent, bg=MainApplication.MODULE_COLOR)
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
        self.errorLabel = tk.Label(self, text=ERROR_MESSAGE, font=LARGE_FONT_BOLD)
        self.errorLabel.grid(row=0, column=1, columnspan=2, pady=10)

    def showPlayerInfo(self):
        self.nameLabel = tk.Label(self, text=self.playerData["name"], font=LARGE_FONT_BOLD)
        self.nameLabel.grid(row=0, column=1, columnspan=2, pady=10)

        self.totalxpLabel = tk.Label(self, text="Total XP: " + str(self.playerData["totalxp"]), font=LARGE_FONT)
        self.totalxpLabel.grid(row=1, column=1, columnspan=2, pady=10)

        self.totalSkillLabel = tk.Label(self, text="Total Level: " + str(self.playerData["totalskill"]),
                                        font=LARGE_FONT)
        self.totalSkillLabel.grid(row=2, column=1, columnspan=2, pady=10)

        self.totalQuestsLabel = tk.Label(self, text="Quests Completed: " + str(self.playerData["completedquests"]),
                                         font=LARGE_FONT)
        self.totalQuestsLabel.grid(row=3, column=1, columnspan=2, pady=10)

        # Track row and column indices for skill labels
        row_index = 4
        column_index = 0

        for skills in self.playerData["skills"]:
            skill_name = skills[0]
            skill_value = str(skills[1])

            # Create and place skill label
            skillLabel = tk.Label(self, text=skill_name + " : " + skill_value, font=SMALL_FONT)
            skillLabel.grid(row=row_index, column=column_index, pady=5, padx=10)

            # Increment row and column indices
            column_index += 1
            if column_index == 4:
                column_index = 0
                row_index += 1
