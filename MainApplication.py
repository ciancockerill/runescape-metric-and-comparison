import tkinter as tk

import PlayerInfoFrame
import playerAPIrequest
import playerData

BACKGROUND_COLOR = "#14294a"
MODULE_COLOR = "#0f2240"


def getWindowWidth(self):
    return self.winfo_width()


def getWindowHeight(self):
    return self.winfo_height()


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.wm_title("Runescape Metrics")
        self.resizable(True, True)
        self.geometry("1280x720")

        self.bgFrame = BGFrame(self)
        self.bgFrame.grid(row=0, column=0, sticky="nsew")

        self.response1 = playerAPIrequest.RequestAPI("possyeggs")
        self.player1 = playerData.PlayerData(self.response1.getPlayerData())

        self.response2 = playerAPIrequest.RequestAPI("kosplink")
        self.player2 = playerData.PlayerData(self.response2.getPlayerData())

        self.playerWidget1 = PlayerWidget(self.bgFrame, self.player1.getFormattedData())
        self.playerWidget1.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky="SW")

        self.playerWidget2 = PlayerWidget(self.bgFrame, self.player2.getFormattedData())
        self.playerWidget2.grid(row=1, column=3, columnspan=2, pady=20, padx=20, rowspan=2, sticky="SE")

        self.player1Search = NameTextEntry(self.bgFrame)
        self.player1Search.grid(row=0, column=0, columnspan=1, pady=10, padx=20, sticky="SW")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.bgFrame.rowconfigure(0, weight=1)
        self.bgFrame.columnconfigure(0, weight=1)

        self.update_idletasks()

    def mainloop(self, n=0):
        super().mainloop()

    def handle_player_search(self, player_name):
        # Update player data and refresh the widget
        response = playerAPIrequest.RequestAPI(player_name)
        player_data = playerData.PlayerData(response.getPlayerData())
        self.playerWidget1.update_data(player_data.getFormattedData())


class BGFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)

        self.parent = parent
        self.update_idletasks()
        self.config(height=parent.winfo_height(), width=parent.winfo_width())


class PlayerWidget(tk.Frame):
    def __init__(self, parent, player_data):
        super().__init__(parent, bg=MODULE_COLOR)
        self.playerData = player_data

        self.update_idletasks()
        self.config(height=parent.winfo_height() // 1.5, width=parent.winfo_width() // 2.5)

        self.infoFrame = PlayerInfoFrame.PlayerInfo(self, self.playerData)
        self.infoFrame.pack(side="top")

    def update_data(self, new_player_data):
        # Destroy the old info frame and create a new one with updated data
        self.infoFrame.destroy()
        self.infoFrame = PlayerInfoFrame.PlayerInfo(self, new_player_data)
        self.infoFrame.pack(side="top")


class NameTextEntry(tk.Entry):
    def __init__(self, parent):
        super().__init__(
            parent,
        )
        self.parent = parent
        self.player_name = None
        self.characterLimit = 12
        self.update_idletasks()
        self.pack_propagate(True)

        self.insert(0, "Enter Name")

        self.bind("<Return>", self.on_enter_pressed)
        self.bind("<Key>", self.on_key_release)

    def handleCharacterLimit(self):
        if len(self.get()) > self.characterLimit:
            self.delete(self.characterLimit, tk.END)

    def on_key_release(self, event):
        self.handleCharacterLimit()

    def on_enter_pressed(self, event):
        playerName = self.get()
        mainapp = self.parent.parent
        mainapp.handle_player_search(playerName)
