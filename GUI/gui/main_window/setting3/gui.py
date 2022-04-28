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


def setting2():
    Setting2()


class Setting2(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.ip=StringVar()
        self.ip.set("กำหนด IP")
        self.password=StringVar()
        self.password.set("1234")
        self.junction=StringVar()
        self.junction.set("เเยกสุขสมาน")

        self.configure(bg="#E0DADA")

        canvas = Canvas(
            self,
            bg="#E0DADA",
            height=670,
            width=980,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=25, y=25)

        


        canvas1 = Canvas(
            self,
            bg="#FFFFFF",
            height=110,
            width=980,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.create_window(0, 0, anchor='nw', window=canvas1)

        canvas1.image_setting_password = PhotoImage(file=relative_to_assets("text_setting_password.png"))
        canvas1.create_image(50, 55.0, image=canvas1.image_setting_password, anchor="w")

        canvas1.entry_text = PhotoImage(file=relative_to_assets("entry_text.png"))
        canvas1.button_entry_text = Button(
            canvas1,
            image=canvas1.entry_text,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("manual"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas1.button_entry_text.place(x=330.0, y=25.0, anchor="nw")

        canvas1.button_password_text = Button(
            canvas1,
            textvariable=self.password,
            font=("Inter", 18 , "bold"),
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changeText(),
            relief="flat",
            bg="#FFFFFF",
            fg="#4F4F4F"
        )
        canvas1.button_password_text.place(x=520.0, y=55.0, anchor="center")

        canvas1.image_button_save = PhotoImage(file=relative_to_assets("bt_save.png"))
        canvas1.button_save = Button(
            canvas1,
            image=canvas1.image_button_save,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("manual"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas1.button_save.place(x=760.0, y=25.0, anchor="nw")




        canvas2 = Canvas(
            self,
            bg="#FFFFFF",
            height=110,
            width=980,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.create_window(0, 135, anchor='nw', window=canvas2)

        canvas2.image_setting_ip = PhotoImage(file=relative_to_assets("text_setting_ip.png"))
        canvas2.create_image(50, 55.0, image=canvas2.image_setting_ip, anchor="w")

        canvas2.entry_text = PhotoImage(file=relative_to_assets("entry_text.png"))
        canvas2.button_entry_text = Button(
            canvas2,
            image=canvas1.entry_text,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("manual"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas2.button_entry_text.place(x=330.0, y=25.0, anchor="nw")

        canvas2.button_ip_text = Button(
            canvas2,
            textvariable=self.ip,
            font=("Inter", 18 , "bold"),
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changeText(),
            relief="flat",
            bg="#FFFFFF",
            fg="#4F4F4F"
        )
        canvas2.button_ip_text.place(x=520.0, y=55.0, anchor="center")

        canvas2.image_button_connect = PhotoImage(file=relative_to_assets("bt_connect.png"))
        canvas2.button_connect = Button(
            canvas2,
            image=canvas2.image_button_connect,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("manual"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas2.button_connect.place(x=760.0, y=25.0, anchor="nw")




        canvas3 = Canvas(
            self,
            bg="#FFFFFF",
            height=110,
            width=980,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.create_window(0, 270, anchor='nw', window=canvas3)

        canvas3.image_setting_junction = PhotoImage(file=relative_to_assets("text_setting_junction.png"))
        canvas3.create_image(50, 55.0, image=canvas3.image_setting_junction, anchor="w")

        canvas3.entry_text = PhotoImage(file=relative_to_assets("entry_text.png"))
        canvas3.button_entry_text = Button(
            canvas3,
            image=canvas3.entry_text,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("manual"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas3.button_entry_text.place(x=330.0, y=25.0, anchor="nw")

        canvas3.button_junction_text = Button(
            canvas3,
            textvariable=self.junction,
            font=("Inter", 18 , "bold"),
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changeText(),
            relief="flat",
            bg="#FFFFFF",
            fg="#4F4F4F"
        )
        canvas3.button_junction_text.place(x=520.0, y=55.0, anchor="center")

        canvas3.image_button_save = PhotoImage(file=relative_to_assets("bt_save.png"))
        canvas3.button_save = Button(
            canvas3,
            image=canvas3.image_button_save,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("manual"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas3.button_save.place(x=760.0, y=25.0, anchor="nw")

        canvas_popup = Canvas(
            self,
            bg="#FFFFFF",
            height=110,
            width=980,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.create_window(0, 270, anchor='nw', window=canvas3)




    def changeText(self):
        self.junction.set("เเยกลาดกระบัง")
      