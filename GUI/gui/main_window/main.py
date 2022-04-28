from pathlib import Path
from tkinter import (
    Label,
    Toplevel,
    Frame,
    Canvas,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
import controller as db_controller
from gui.main_window.dashboard.gui import Dashboard
from gui.main_window.fixtimeTabel.gui import FixtimeTabel
from gui.main_window.reservations.main import Reservations
from gui.main_window.about.main import About
from gui.main_window.rooms.main import Rooms
from gui.main_window.guests.main import Guests
from gui.main_window.setting.main import Setting
from .. import login
import socket_controller as socketIO

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def mainWindow():
    MainWindow()


class MainWindow(Toplevel):
    global user

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.title("Area Traffic Management System")
        self.geometry("1280x720")
        self.bind("<Escape>", self.Quit)
        self.attributes('-fullscreen',True)
        self.config(cursor="none") # remove cursor 
        # self.wm_attributes("-topmost", 1)

        self.configure(bg="#E0DADA")

        self.current_window = None

        self.windows = {
            "main": Main(self),
            "login": Login(self),
        }

        self.handle_btn_press("login")

        self.current_window.place(x=0, y=0, width=1280.0, height=720.0)

        self.current_window.tkraise()

        self.resizable(False, False)
        self.mainloop()


    def handle_btn_press(self, name):
        # Hide all screens
        for window in self.windows.values():
            window.place_forget()
        
        self.current_window = self.windows.get(name)

        # Show the screen of the button pressed
        self.windows[name].place(x=0, y=0, width=1280.0, height=720.0)

        if name == 'main':
            self.windows['main'].handle_btn_press(self.windows['main'].dashboard_btn,'main')

    def Quit(self,event):
        socketIO.disconnect()
        quit()

class Main(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.current_window = None
        self.current_window_label = StringVar()

        self.canvas = Canvas(
            self,
            bg="#5F95FF",
            height=720,
            width=250,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

        self.sidebar_indicator = Frame(self, background="#FFFFFF")

        self.sidebar_indicator.place(x=0, y=120, height=60, width=10)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_home.png"))
        self.dashboard_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.dashboard_btn, "main"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.dashboard_btn.place(x=1, y=120.0, width=250.0, height=60.0)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_setting.png"))
        self.setting_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.setting_btn, "setting"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.setting_btn.place(x=1, y=180.0, width=250.0, height=60.0)

        self.button_image_logout = PhotoImage(file=relative_to_assets("button_logout.png"))
        self.logout_btn = Button(
            self.canvas,
            image=self.button_image_logout,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.logout(),
            relief="flat",
        )
        self.logout_btn.place(x=1.0, y=240.0, width=250.0, height=60.0)

        self.canvas.create_text(
            40.0,
            37.0,
            anchor="nw",
            text="ATMS",
            fill="#FFFFFF",
            font=("Inter", 40 ,"bold"),
        )

        self.windows = {
            "main": Dashboard(self),
            "setting": Setting(self),
            "tabel": FixtimeTabel(self),
            "gue": Guests(self),
            "abt": About(self),
            "res": Reservations(self),
        }

        self.handle_btn_press(self.dashboard_btn, "main")
        self.sidebar_indicator.place(x=0, y=120)

        self.current_window.place(x=250, y=0, width=1030.0, height=720.0)

        self.current_window.tkraise()
    

    def place_sidebar_indicator(self):
        pass

    def handle_btn_press(self, caller, name):
        # Place the sidebar on respective button
        self.sidebar_indicator.place(x=0, y=caller.winfo_y())

        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Set ucrrent Window
        self.current_window = self.windows.get(name)

        # Show the screen of the button pressed
        self.windows[name].place(x=250, y=0, width=1030, height=720.0)

        if name == 'main':
            self.windows[name].navigate('main')

        elif name == 'setting':
            self.windows[name].navigate('main')

        # Handle label change
        # current_name = self.windows.get(name)._name.split("!")[-1].capitalize()
        # self.canvas.itemconfigure(self.heading, text=current_name)

    def handle_dashboard_refresh(self):
        # Recreate the dash window
        self.windows["dash"] = Dashboard(self)

    def logout(self):
        confirm = messagebox.askokcancel(
            "Confirm logout", "คุณต้องการออกจากระบบใช่หรือไม่"
        )
        if confirm == True:
            self.parent.handle_btn_press("login")



class Login(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#5F95FF")

        self.password=StringVar()
        self.password.set("")

        self.canvas = Canvas(
            self,
            bg="#5F95FF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_text(
            40.0,
            37.0,
            anchor="nw",
            text="ATMS",
            fill="#FFFFFF",
            font=("Inter", 40 ,"bold"),
        )

        canvas1 = Canvas(
            self,
            bg="#FFFFFF",
            height=720,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas1.place(x=640, y=0, anchor="n")

        canvas1.image_text_password = PhotoImage(file=relative_to_assets("text_password.png"))
        canvas1.create_image(300, 35, image=canvas1.image_text_password, anchor="n")

        canvas1.entry_text = PhotoImage(file=relative_to_assets("entry_text.png"))
        canvas1.create_image(300, 90.0, image=canvas1.entry_text, anchor="n")

        canvas1.label_password = Label(
            canvas1,
            anchor="n",
            font=("Inter", 18 , "bold"),
            textvariable=self.password,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        canvas1.label_password.place(x=300, y=120, anchor="center")

        canvas_numpad = Canvas(
                self,
                bg="#FFFFFF",
                height=400,
                width=295,
                bd=0,
                highlightthickness=0,
                relief="ridge",
        )
        canvas1.create_window(300, 175, anchor='n', window=canvas_numpad)

        canvas_numpad.image_number_dot = PhotoImage(file=relative_to_assets("number_dot.png"))
        canvas_numpad.image_number_del = PhotoImage(file=relative_to_assets("number_del.png"))
        canvas_numpad.image_number_0 = PhotoImage(file=relative_to_assets("number_0.png"))
        canvas_numpad.image_number_1 = PhotoImage(file=relative_to_assets("number_1.png"))
        canvas_numpad.image_number_2 = PhotoImage(file=relative_to_assets("number_2.png"))
        canvas_numpad.image_number_3 = PhotoImage(file=relative_to_assets("number_3.png"))
        canvas_numpad.image_number_4 = PhotoImage(file=relative_to_assets("number_4.png"))
        canvas_numpad.image_number_5 = PhotoImage(file=relative_to_assets("number_5.png"))
        canvas_numpad.image_number_6 = PhotoImage(file=relative_to_assets("number_6.png"))
        canvas_numpad.image_number_7 = PhotoImage(file=relative_to_assets("number_7.png"))
        canvas_numpad.image_number_8 = PhotoImage(file=relative_to_assets("number_8.png"))
        canvas_numpad.image_number_9 = PhotoImage(file=relative_to_assets("number_9.png"))
        
        canvas_numpad.number_dot = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_dot,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("."),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_dot.place(x=0.0, y=315.0, anchor="nw")

        canvas_numpad.number_del = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_del,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("del"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_del.place(x=210.0, y=315.0, anchor="nw")

        canvas_numpad.number_0 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("0"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_0.place(x=105.0, y=315.0, anchor="nw")

        canvas_numpad.number_1 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("1"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_1.place(x=0.0, y=210.0, anchor="nw")

        canvas_numpad.number_2 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("2"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_2.place(x=105.0, y=210.0, anchor="nw")

        canvas_numpad.number_3 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("3"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_3.place(x=210.0, y=210.0, anchor="nw")

        canvas_numpad.number_4 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("4"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_4.place(x=0.0, y=105.0, anchor="nw")

        canvas_numpad.number_5 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("5"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_5.place(x=105.0, y=105.0, anchor="nw")

        canvas_numpad.number_6 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("6"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_6.place(x=210.0, y=105.0, anchor="nw")

        canvas_numpad.number_7 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("7"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_7.place(x=0.0, y=0.0, anchor="nw")

        canvas_numpad.number_8 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("8"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_8.place(x=105.0, y=0.0, anchor="nw")

        canvas_numpad.number_9 = Button(
            canvas_numpad,
            image=canvas_numpad.image_number_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_press_number("9"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas_numpad.number_9.place(x=210.0, y=0.0, anchor="nw")

        canvas1.image_login = PhotoImage(file=relative_to_assets("button_login.png"))
        canvas1.button_login = Button(
            canvas1,
            image=canvas1.image_login,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.login(),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas1.button_login.place(x=300, y=595.0, anchor="n")


    def on_press_number(self,value):
        if value != 'del':
            self.password.set(self.password.get()+value)
        else:
            self.password.set(self.password.get()[:-1])
    def reset(self):
        self.password.set("")
        

    def login(self):
        if self.checkPassword(self.password.get()):
            self.parent.handle_btn_press("main")
        else:
            messagebox.showerror(
                title="Invalid Password",
                message="รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง",
            )
        self.reset()

    def checkPassword(self,password):
        return db_controller.checkPassword(password)