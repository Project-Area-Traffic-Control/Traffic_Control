from pathlib import Path
import time
from tkinter.constants import ANCHOR, N
from gui.main_window.dashboard.junction_image.main import JunctionImage
# from matplotlib.figure import Figure
from gui.main_window.dashboard.operation_main.main import OperationMain
from gui.main_window.dashboard.operation_manual.main import OperationManual
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Button, Frame, Canvas, Entry, Label, PhotoImage, N, StringVar, messagebox
# import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def fixtimeTabel():
    FixtimeTabel()


class FixtimeTabel(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#E0DADA")

        
      