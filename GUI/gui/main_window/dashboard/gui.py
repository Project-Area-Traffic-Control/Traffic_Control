import datetime
from itertools import count
from pathlib import Path
import time
from tkinter.constants import ANCHOR, N
from gui.main_window.dashboard.junction_image.main import JunctionImage
# from matplotlib.figure import Figure
from gui.main_window.dashboard.operation_main.main import OperationMain
from gui.main_window.dashboard.operation_manual.main import OperationManual
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Button, Frame, Canvas, Entry, Label, PhotoImage, N, StringVar, messagebox
import controller as db_controller
import socket_controller as socket
import global_data as GlobalData

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def dashboard():
    Dashboard()


class Dashboard(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#E0DADA")

        self.numberOfJunction = 4
        self.current_mode = "auto"
        self.current_phase = 1

        self.temp_time = 0

        self.operation_windows = {
            "main" : OperationMain(self),
            "manual" : OperationManual(self)
        }

        self.current_operation_window = self.operation_windows["main"]
        self.current_operation_window.place(x=25, y=25, width=380.0, height=670.0)

        self.current_operation_window.tkraise()

        junctionImage = JunctionImage(self)
        junctionImage.place(x=430, y=120, width=575.0, height=575.0)
        junctionImage.tkraise()



        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=70,
            width=575,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=430, y=25)

        canvas.image_text_time = PhotoImage(file=relative_to_assets("text_time.png"))
        canvas.create_image(25, 35, image=canvas.image_text_time, anchor="w")

        canvas.entry_image_time = PhotoImage(file=relative_to_assets("entry_time.png"))
        canvas.create_image(140.0, 35, image=canvas.entry_image_time, anchor="w")

        canvas.image_text_sec = PhotoImage(file=relative_to_assets("text_sec.png"))
        canvas.create_image(265, 35, image=canvas.image_text_sec, anchor="w")

        canvas.image_state_connect = PhotoImage(file=relative_to_assets("state_disconnected.png"))
        self.label_state_connect = Label(canvas, image=canvas.image_state_connect, bg="#FFFFFF")
        self.label_state_connect.place(x=405, y=35, anchor="w")

        self.second=StringVar()
        self.second.set("120")
    
        self.label_time = Label(
            canvas,
            anchor="center",
            font=("Inter", 20 , "bold"),
            textvariable=self.second,
            bg="#528CFF",  
            fg="#FFFFFF"
        )
        self.label_time.place(x=190, y=35, anchor="center")
        self.connect_to_server()
        self.loop()
        self.updateSecond()
        

    def navigate(self, name):
        # Hide all screens
        for operation_windows in self.operation_windows.values():
            operation_windows.place_forget()

        # Show the screen of the button pressed
        self.operation_windows[name].place(x=25, y=25, width=380.0, height=670.0)

    def change_img_connected(self,state):
        global path
        if state:
            path = "state_connected.png"
        else:
            path =  "state_disconnected.png"

        new_img=PhotoImage(file=relative_to_assets(path))
        self.label_state_connect.configure(image=new_img)
        self.label_state_connect.image = new_img

    def changeMode(self,mode):
        if mode == "manual":
            self.operation_windows["manual"].disable(self.numberOfJunction,False)
        else:
            self.operation_windows["manual"].disable(self.numberOfJunction,True)
    
    def updateSecond(self):
        sec = GlobalData.timer
        self.second.set("{0:3d}".format(sec))
        self.label_time.config(text=self.second)
        self.label_time.after(500,self.updateSecond)

    def connect_to_server(self):
        ip = GlobalData.ip_server
        try:
            if not socket.getStatus():
                socket.connect(ip)
                self.change_img_connected(True)

        except Exception as err: 
            print(err)



    def loop(self):
        self.change_img_connected(socket.getStatus())
        self.connect_to_server()
        self.label_time.after(2000,self.loop)
       