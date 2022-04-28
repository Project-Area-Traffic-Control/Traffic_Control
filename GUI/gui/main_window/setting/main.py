from pathlib import Path

from tkinter import Frame, Canvas, Entry, StringVar, Text, Button, PhotoImage, messagebox
from gui.main_window.setting.edit_ip.main import Edit_ip
from gui.main_window.setting.edit_junction.main import Edit_junction
from gui.main_window.setting.edit_password.gui import Edit_password

from gui.main_window.setting.setting_main.gui import Setting_main
import controller as db_controller



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def setting():
    Setting()


class Setting(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.ip=StringVar()
        self.password=StringVar()
        self.junction=StringVar()
        self.loadData()

        self.configure(bg="#E0DADA")

        # Loop through windows and place them
        self.windows = {
            "main": Setting_main(self),
            "edit_ip": Edit_ip(self),
            "edit_junction": Edit_junction(self),
            "edit_password": Edit_password(self),
        }

        self.current_window = self.windows["main"]
        self.current_window.place(x=25, y=25, width=980.0, height=670.0)

        self.current_window.tkraise()

    def navigate(self, name):
        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Show the screen of the button pressed
        self.windows[name].place(x=25, y=25, width=980.0, height=670.0)

        if name == "edit_password":
            self.windows[name].reset_new_value()
        elif name == "edit_ip":
            self.windows[name].reset_new_value()

    def loadData(self):
        password = db_controller.getPassword()
        ip = db_controller.getIP()
        self.password.set(password)
        self.junction.set("เเยกสุขสมาน")
        if ip != '':
            self.ip.set(ip)
        else:
            self.ip.set('กำหนด IP')
