import tkinter as tk
import threading
import queue

import comparing
import player_data_widget
import player_api_request
import player_data
import image_loader

BACKGROUND_COLOR = "#14294a"
MODULE_COLOR = "#0f2240"

# Default searches when application opens
DEFAULT_SEARCH1 = "possyeggs"
DEFAULT_SEARCH2 = "kosplink"


def requestPlayerTable(playerName, data_queue):
    responseData = player_api_request.RequestAPI(playerName).getPlayerData()
    if responseData:
        playerTable = player_data.PlayerData(responseData).getFormattedData()
    else:
        playerTable = None

    # Put the result in the queue
    data_queue.put(playerTable)


class MainApplication(tk.Tk):
    skillImageDirectories = image_loader.ImageLoader().getImageDirectories()

    def __init__(self):
        super().__init__()
        self.withdraw()  # Hide the window
        self.after(0, self.deiconify)  # After the window has fully loaded, show again

        self.__configure_grid()

        self.wm_title("Runescape 3 Player Metrics & Comparison")
        self.resizable(True, True)
        self.geometry("1280x720")
        self.configure(bg=BACKGROUND_COLOR)

        self.__initPlayerWidgets()
        self.__initPlayerSearchBoxes()
        self.__initPlayerLabels()

        self.after(3000, self.comparePlayers)

        self.update_idletasks()

    def mainloop(self, n=0):
        super().mainloop()

    def comparePlayers(self):
        p1_skillWidget = self.playerWidget1.infoFrame
        p2_skillWidget = self.playerWidget2.infoFrame

        if (p1_skillWidget is None) or (p2_skillWidget is None):
            return

        compare = comparing.CompareStats(p1_skillWidget, p2_skillWidget)
        compare.compareSkills()

    def __initPlayerWidgets(self):
        self.playerWidget1 = self.addPlayerInfoBox(DEFAULT_SEARCH1)
        self.playerWidget1.grid(row=2, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")

        self.playerWidget2 = self.addPlayerInfoBox(DEFAULT_SEARCH2)
        self.playerWidget2.grid(row=2, column=3, columnspan=3, pady=20, padx=20, sticky="nsew")

    def __initPlayerSearchBoxes(self):
        self.player1Search = NameTextEntry(self, self.playerWidget1)
        self.player1Search.grid(row=1, column=1, sticky="ew")

        self.player2Search = NameTextEntry(self, self.playerWidget2)
        self.player2Search.grid(row=1, column=4, sticky="ew")

    def __initPlayerLabels(self):
        self.player1Label = tk.Label(text="Enter Player Name", font=player_data_widget.LARGE_FONT, pady=10,
                                     bg=BACKGROUND_COLOR, fg="white")
        self.player1Label.grid(row=0, column=1, sticky="ew")

        self.player2Label = tk.Label(text="Enter Player Name", font=player_data_widget.LARGE_FONT, pady=10,
                                     bg=BACKGROUND_COLOR, fg="white")
        self.player2Label.grid(row=0, column=4, sticky="ew")

    def __configure_grid(self):
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=2)

        for i in range(6):
            self.columnconfigure(i, weight=1)

    def addPlayerInfoBox(self, playerName):
        # Spawn the playerWidget
        playerWidget = PlayerWidget(self, None)

        # Create a queue for API request results
        data_queue = queue.Queue()

        # Start the thread to fetch the player data
        requestThread = threading.Thread(target=requestPlayerTable, args=(playerName, data_queue))
        requestThread.start()

        # Schedule the queue check method
        self.after(100, self.process_queue, data_queue, playerWidget)
        return playerWidget

    def process_queue(self, data_queue, playerWidget):
        try:
            playerTable = data_queue.get_nowait()
        except queue.Empty:
            # If queue empty, try again after 100ms
            self.after(100, self.process_queue, data_queue, playerWidget)
        else:
            # API data received, update the playerWidget
            playerWidget.update_data(playerTable)

            if playerTable is not None:
                self.comparePlayers()


class PlayerWidget(tk.Frame):
    def __init__(self, parent, player_data):
        super().__init__(parent, bg=MODULE_COLOR)
        self.parent = parent
        self.playerData = player_data
        self.loadingLabel = None
        self.infoFrame = None

        if self.playerData is None:
            self.showLoading()

        self.update_idletasks()

    def update_data(self, new_player_data):
        # Destroy the old info frame and create a new one with updated data
        if self.loadingLabel is not None:
            self.loadingLabel.destroy()
        if self.infoFrame is not None:
            self.infoFrame.destroy()

        self.infoFrame = player_data_widget.PlayerInfo(self, new_player_data)
        self.infoFrame.pack(side="top")

    def handle_player_search(self, player_name):
        # Show loading indicator and start a thread to handle player search
        self.showLoading()
        data_queue = queue.Queue()
        threading.Thread(target=requestPlayerTable, args=(player_name, data_queue)).start()
        self.parent.after(100, self.parent.process_queue, data_queue, self)

    def showLoading(self):
        self.loadingLabel = tk.Label(self, text="Loading...", font=player_data_widget.LARGE_FONT)
        self.loadingLabel.pack()


class NameTextEntry(tk.Entry):
    def __init__(self, parent, playerWidget):
        super().__init__(parent)
        self.parent = parent
        self.player_name = None
        self.characterLimit = 12
        self.update_idletasks()
        self.pack_propagate(True)
        self.playerWidget = playerWidget

        self.insert(0, "")

        self.bind("<Return>", self.on_enter_pressed)
        self.bind("<Key>", self.on_key_release)

    def handleCharacterLimit(self):  # deletes chars that extend the max char limit
        if len(self.get()) > self.characterLimit:
            self.delete(self.characterLimit, tk.END)

    def on_key_release(self, event):
        self.handleCharacterLimit()

    def on_enter_pressed(self, event):
        playerName = self.get()
        self.playerWidget.handle_player_search(playerName)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
