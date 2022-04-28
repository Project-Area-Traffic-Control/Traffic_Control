from logging import disable
from pathlib import Path
# import controller as db_controller

from tkinter import (
    Frame,
    Canvas,
    Entry,
    Text,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
from tkinter.ttk import Treeview

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def edit_junction():
    Edit_junction()


class Edit_junction(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
  