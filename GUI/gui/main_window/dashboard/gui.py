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


def dashboard():
    Dashboard()


class Dashboard(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#E0DADA")

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


        # canvas3 = Canvas(
        #     self,
        #     bg="#FFFFFF",
        #     height=575,
        #     width=575,
        #     bd=0,
        #     highlightthickness=0,
        #     relief="ridge",
        # )
        # canvas3.place(x=430, y=120)

        # canvas3.image_junction = PhotoImage(file=relative_to_assets("4way0degree.png"))

        # self.label_image_junction = Label(canvas3,image=canvas3.image_junction,bg="#FFFFFF")
        # self.label_image_junction.place(x=287.5,y=287.5,anchor='center')





    def onAuto(self):
        self.change_img_bt("auto")
    def onMaual(self):
        self.change_img_bt("manual")
        self.change_state_connect("disconnect")
    def onRed(self):
        self.change_img_bt("red")
        self.change_state_connect("connect")
    def onFlashing(self):
        self.change_img_bt("flashing")
        self.countdown()
    
    def navigate(self, name):
        # Hide all screens
        for operation_windows in self.operation_windows.values():
            operation_windows.place_forget()

        # Show the screen of the button pressed
        self.operation_windows[name].place(x=25, y=25, width=380.0, height=670.0)

    def click(self):
        print("click....")

    def change_state_connect(self,state):
        global path
        if state == "connect":
            path = "state_connected.png"
        elif state == "disconnect":
            path =  "state_disconnected.png"

        new_img=PhotoImage(file=relative_to_assets(path))
        self.label_state_connect.configure(image=new_img)
        self.label_state_connect.image = new_img
    
    def setPlanName(self,new_name):
        self.plan_name.set(new_name)
    
    def countdown(self):
        sec = int(self.second.get())
        
        if sec > 0:
            sec -= 1
            self.second.set("{0:3d}".format(sec))
            self.label_time.config(text=self.second)
            self.label_time.after(1000,self.countdown)

    def countdown1(self):
        
        try:
            temp =  int(self.second.get())
        except:
            print("Please input the right value")
        while temp >-1:
     
            secs = temp
    
      
            self.second.set("{0:3d}".format(secs))
    
            self.update()
            time.sleep(1)

            # if (temp == 0):
            #     messagebox.showinfo("Time Countdown", "Time's up ")
            
            temp -= 1



        # # Vacant Text
        # canvas.create_text(
        #     164.0,
        #     63.0,
        #     anchor="ne",
        #     text=db_controller.vacant(),
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 48 * -1),
        #     justify="right",
        # )

        # canvas.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        # entry_bg_2 = canvas.create_image(299.0, 81.0, image=canvas.entry_image_2)
        # entry_2 = Entry(
        #     self,
        #     bd=0,
        #     bg="#EFEFEF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_2.place(x=239.0, y=30.0 + 2, width=120.0, height=0)

        # canvas.create_text(
        #     240.0,
        #     45.0,
        #     anchor="nw",
        #     text="Booked",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 14 * -1),
        # )

        # canvas.create_text(
        #     346.0,
        #     63.0,
        #     anchor="ne",
        #     text=db_controller.booked(),
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 48 * -1),
        #     justify="right",
        # )

        # canvas.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        # entry_bg_3 = canvas.create_image(177.0, 286.0, image=canvas.entry_image_3)
        # entry_3 = Entry(
        #     self,
        #     bd=0,
        #     bg="#EFEFEF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_3.place(x=55.0, y=175.0 + 2, width=244.0, height=0)

        # canvas.entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
        # entry_bg_4 = canvas.create_image(481.0, 286.0, image=canvas.entry_image_4)
        # entry_4 = Entry(
        #     self,
        #     bd=0,
        #     bg="#EFEFEF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_4.place(x=358.0, y=175.0 + 2, width=246.0, height=0)

        # canvas.entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
        # entry_bg_5 = canvas.create_image(221.0, 207.5, image=canvas.entry_image_5)
        # entry_5 = Entry(
        #     self,
        #     bd=0,
        #     bg="#5E95FF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_5.place(x=219.5, y=202.0 + 2, width=3.0, height=0)

        # canvas.entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
        # entry_bg_6 = canvas.create_image(221.0, 230.5, image=canvas.entry_image_6)
        # entry_6 = Entry(
        #     self,
        #     bd=0,
        #     bg="#777777",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_6.place(x=219.5, y=225.0 + 2, width=3.0, height=0)

        # canvas.create_text(
        #     235.0,
        #     200.0,
        #     anchor="nw",
        #     text="Booked",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 13 * -1),
        # )

        # canvas.create_text(
        #     235.0,
        #     222.0,
        #     anchor="nw",
        #     text="Vacant",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 13 * -1),
        # )

        # canvas.entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
        # entry_bg_7 = canvas.create_image(483.0, 81.0, image=canvas.entry_image_7)
        # entry_7 = Entry(
        #     self,
        #     bd=0,
        #     bg="#EFEFEF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_7.place(x=423.0, y=30.0 + 2, width=120.0, height=0)

        # canvas.create_text(
        #     424.0,
        #     45.0,
        #     anchor="nw",
        #     text="Hotel Value",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 14 * -1),
        # )

        # canvas.create_text(
        #     540.0,
        #     63.0,
        #     anchor="ne",
        #     text=db_controller.get_total_hotel_value(),
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 48 * -1),
        # )

        # canvas.entry_image_8 = PhotoImage(file=relative_to_assets("entry_8.png"))
        # entry_bg_8 = canvas.create_image(667.0, 81.0, image=canvas.entry_image_8)
        # entry_8 = Entry(
        #     self,
        #     bd=0,
        #     bg="#EFEFEF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_8.place(x=607.0, y=30.0 + 2, width=120.0, height=0)

        # canvas.create_text(
        #     608.0,
        #     45.0,
        #     anchor="nw",
        #     text="Meals Taken",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 14 * -1),
        # )

        # canvas.create_text(
        #     712.0,
        #     63.0,
        #     anchor="ne",
        #     text=db_controller.meals(),
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 48 * -1),
        # )

        # canvas.entry_image_9 = PhotoImage(file=relative_to_assets("entry_9.png"))
        # entry_bg_9 = canvas.create_image(391.0, 150.0, image=canvas.entry_image_9)
        # entry_9 = Entry(
        #     self,
        #     bd=0,
        #     bg="#EFEFEF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_9.place(x=41.0, y=149.0 + 2, width=700.0, height=0)

        # canvas.create_text(
        #     56.0,
        #     191.0,
        #     anchor="nw",
        #     text="Room",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 26 * -1),
        # )

        # canvas.create_text(
        #     56.0,
        #     223.0,
        #     anchor="nw",
        #     text="Status",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 18 * -1),
        # )

        # canvas.create_text(
        #     359.0,
        #     223.0,
        #     anchor="nw",
        #     text="By Type",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 18 * -1),
        # )

        # canvas.create_text(
        #     359.0,
        #     191.0,
        #     anchor="nw",
        #     text="Bookings",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 26 * -1),
        # )

        # canvas.entry_image_10 = PhotoImage(file=relative_to_assets("entry_10.png"))
        # entry_bg_10 = canvas.create_image(251.0, 218.5, image=canvas.entry_image_10)
        # entry_10 = Entry(
        #     self,
        #     bd=0,
        #     bg="#FFFFFF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_10.place(x=219.0, y=186.0 + 2, width=64.0, height=0)

        # canvas.entry_image_11 = PhotoImage(file=relative_to_assets("entry_11.png"))
        # entry_bg_11 = canvas.create_image(221.0, 207.5, image=canvas.entry_image_11)
        # entry_11 = Entry(
        #     self,
        #     bd=0,
        #     bg="#5E95FF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_11.place(x=219.5, y=202.0 + 2, width=3.0, height=0)

        # canvas.entry_image_12 = PhotoImage(file=relative_to_assets("entry_12.png"))
        # entry_bg_12 = canvas.create_image(221.0, 230.5, image=canvas.entry_image_12)
        # entry_12 = Entry(
        #     self,
        #     bd=0,
        #     bg="#777777",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_12.place(x=219.5, y=225.0 + 2, width=3.0, height=0)

        # canvas.create_text(
        #     235.0,
        #     200.0,
        #     anchor="nw",
        #     text="Vacant",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 13 * -1),
        # )

        # canvas.create_text(
        #     235.0,
        #     222.0,
        #     anchor="nw",
        #     text="Booked",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 13 * -1),
        # )

        # canvas.entry_image_13 = PhotoImage(file=relative_to_assets("entry_13.png"))
        # entry_bg_13 = canvas.create_image(
        #     555.693603515625, 218.5, image=canvas.entry_image_13
        # )
        # entry_13 = Entry(
        #     self,
        #     bd=0,
        #     bg="#FFFFFF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_13.place(x=523.693603515625, y=186.0 + 2, width=64.0, height=0)

        # canvas.entry_image_14 = PhotoImage(file=relative_to_assets("entry_14.png"))
        # entry_bg_14 = canvas.create_image(
        #     525.693603515625, 207.5, image=canvas.entry_image_14
        # )
        # entry_14 = Entry(
        #     self,
        #     bd=0,
        #     bg="#5E95FF",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_14.place(x=524.193603515625, y=202.0 + 2, width=3.0, height=0)

        # canvas.entry_image_15 = PhotoImage(file=relative_to_assets("entry_15.png"))
        # entry_bg_15 = canvas.create_image(
        #     525.693603515625, 230.5, image=canvas.entry_image_15
        # )
        # entry_15 = Entry(
        #     self,
        #     bd=0,
        #     bg="#777777",
        #     highlightthickness=0,
        #     font=("Montserrat Bold", 150),
        # )
        # entry_15.place(x=524.193603515625, y=225.0 + 2, width=3.0, height=0)

        # canvas.create_text(
        #     539.693603515625,
        #     200.0,
        #     anchor="nw",
        #     text="Delux",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 13 * -1),
        # )

        # canvas.create_text(
        #     539.693603515625,
        #     222.0,
        #     anchor="nw",
        #     text="Normal",
        #     fill="#5E95FF",
        #     font=("Montserrat Bold", 13 * -1),
        # )

        # canvas.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        # image_1 = canvas.create_image(726.0, 298.0, image=canvas.image_image_1)

        # fig = Figure(figsize=(2.2, 1.30), dpi=100)
        # fig.patch.set_facecolor("#eeefee")

        # plot1 = fig.add_subplot(111)
        # plot1.pie(
        #     [db_controller.vacant(), db_controller.booked()],
        #     [0.1, 0.1],
        #     startangle=-30,
        #     colors=("#6495ED", "#8A8A8A"),
        # )

        # canvas1 = FigureCanvasTkAgg(fig, self)
        # canvas1.draw()
        # canvas1.get_tk_widget().place(x=57, y=253)

        # fig1 = Figure(figsize=(2.2, 1.30), dpi=100)
        # fig1.patch.set_facecolor("#eeefee")

        # plot2 = fig1.add_subplot(111)
        # plot2.pie([5, 3], [0.1, 0.1], startangle=-30, colors=("#6495ED", "#8A8A8A"))

        # canvas2 = FigureCanvasTkAgg(fig1, self)
        # canvas2.draw()
        # canvas2.get_tk_widget().place(x=359, y=253)
