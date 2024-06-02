import tkinter as tk

import PlayerInfoFrame
import playerAPIrequest
import playerData
import ImageLoader

BACKGROUND_COLOR = "#14294a"
MODULE_COLOR = "#0f2240"


class MainApplication(tk.Tk):
    skillDirectories = ImageLoader.ImageLoader().getImageDirectories()

    def __init__(self):
        super().__init__()

        self.wm_title("Runescape Metrics")
        self.resizable(True, True)
        self.geometry("1280x720")
        self.configure(bg=BACKGROUND_COLOR)

        self.response1 = playerAPIrequest.RequestAPI("possyeggs")
        self.player1 = playerData.PlayerData(self.response1.getPlayerData())

        self.response2 = playerAPIrequest.RequestAPI("kosplink")
        self.player2 = playerData.PlayerData(self.response2.getPlayerData())

        self.playerWidget1 = PlayerWidget(self, self.player1.getFormattedData())
        self.playerWidget1.grid(row=2, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")

        self.playerWidget2 = PlayerWidget(self, self.player2.getFormattedData())
        self.playerWidget2.grid(row=2, column=3, columnspan=3, pady=20, padx=20, sticky="nsew")

        self.player1Search = NameTextEntry(self, self.playerWidget1)
        self.player1Search.grid(row=1, column=1, sticky="ew")

        self.player2Search = NameTextEntry(self, self.playerWidget2)
        self.player2Search.grid(row=1, column=4, sticky="ew")

        self.__configure_grid()
        self.update_idletasks()

    def mainloop(self, n=0):
        super().mainloop()

    def __configure_grid(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=2)

        for i in range(6):
            self.columnconfigure(i, weight=1)


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

    def __update_data(self, new_player_data):
        # Destroy the old info frame and create a new one with updated data
        self.infoFrame.destroy()
        self.infoFrame = PlayerInfoFrame.PlayerInfo(self, new_player_data)
        self.infoFrame.pack(side="top")

    def handle_player_search(self, player_name):
        response = playerAPIrequest.RequestAPI(player_name)
        player_data = playerData.PlayerData(response.getPlayerData())
        self.__update_data(player_data.getFormattedData())


class NameTextEntry(tk.Entry):
    def __init__(self, parent, playerWidget):
        super().__init__(
            parent,
        )
        self.parent = parent
        self.player_name = None
        self.characterLimit = 12
        self.update_idletasks()
        self.pack_propagate(True)
        self.playerWidget = playerWidget

        self.insert(0, "")

        self.bind("<Return>", self.on_enter_pressed)
        self.bind("<Key>", self.on_key_release)

    def handleCharacterLimit(self):
        if len(self.get()) > self.characterLimit:
            self.delete(self.characterLimit, tk.END)

    def on_key_release(self, event):
        self.handleCharacterLimit()

    def on_enter_pressed(self, event):
        playerName = self.get()
        self.playerWidget.handle_player_search(playerName)
