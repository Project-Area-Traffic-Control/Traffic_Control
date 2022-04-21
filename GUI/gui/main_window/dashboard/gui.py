from pathlib import Path
import time
from tkinter.constants import ANCHOR, N
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

        self.plan_name=StringVar()
        self.plan_name.set("ช่วงเช้า 6 - 8 โมง")

        self.image_auto_off = PhotoImage(file=relative_to_assets("auto_bt_off.png"))
        self.image_auto_on = PhotoImage(file=relative_to_assets("auto_bt_on.png"))
        self.image_manual_off = PhotoImage(file=relative_to_assets("manual_bt_off.png"))
        self.image_manual_on = PhotoImage(file=relative_to_assets("manual_bt_on.png"))
        self.image_red_off = PhotoImage(file=relative_to_assets("red_bt_off.png"))
        self.image_red_on = PhotoImage(file=relative_to_assets("red_bt_on.png"))
        self.image_flashing_off = PhotoImage(file=relative_to_assets("flashing_bt_off.png"))
        self.image_flashing_on = PhotoImage(file=relative_to_assets("flashing_bt_on.png"))

        canvas1 = Canvas(
            self,
            bg="#FFFFFF",
            height=561,
            width=293,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas1.place(x=21, y=17)
  
        canvas1.create_text(
            146.5,
            35.0,
            anchor="center",
            text="โหมดการทำงาน",
            fill="#5E95FF",
            font=("Montserrat Bold", 24 * -1),
        )

        self.button_auto = Button(
            self,
            image=self.image_auto_on,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.onAuto(),
            relief="flat",
        )
        self.button_auto.place(x=98.0, y=108.0, width=131.0, height=40.0)

        self.button_manual = Button(
            self,
            image=self.image_manual_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.onMaual(),
            relief="flat",
        )
        self.button_manual.place(x=98.0, y=165.0, width=131.0, height=40.0)

        self.button_red = Button(
            self,
            image=self.image_red_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.onRed(),
            relief="flat",
        )
        self.button_red.place(x=98.0, y=222.0, width=131.0, height=40.0)

        self.button_flashing = Button(
            self,
            image=self.image_flashing_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.onFlashing(),
            relief="flat",
        )
        self.button_flashing.place(x=98.0, y=279.0, width=131.0, height=40.0)

        canvas1.create_text(
            146.5,
            361.0,
            anchor="center",
            text="เเผนการทำงานปัจจุบัน",
            fill="#5E95FF",
            font=("Montserrat Bold", 24 * -1),
        )

        label_plan_name = Label(
            self,
            anchor="center",
            font=("Montserrat Bold", 18 * -1),
            textvariable=self.plan_name,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        label_plan_name.place(x=166.5, y=417,anchor="center")

        canvas1.create_text(
            146.5,
            470.0,
            anchor="center",
            text="เวลาปัจจุบัน",
            fill="#5E95FF",
            font=("Montserrat Bold", 24 * -1),
        )

        self.label_timer = Label(
            self,
            anchor="center",
            font=("Montserrat Bold", 18 * -1),
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        self.label_timer.place(x=166.5, y=525,anchor="center")
        self.my_time()



        canvas2 = Canvas(
            self,
            bg="#FFFFFF",
            height=70,
            width=470,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas2.place(x=334, y=17)

        canvas2.create_text(
            22.0,
            20.0,
            anchor="nw",
            text="ระยะเวลา",
            fill="#5E95FF",
            font=("Montserrat Bold", 20 * -1),
        )
        canvas2.create_text(
            232.0,
            20.0,
            anchor="nw",
            text="วินาที",
            fill="#5E95FF",
            font=("Montserrat Bold", 20 * -1),
        )

        canvas2.entry_image_state_connect = PhotoImage(file=relative_to_assets("state_disconnected.png"))

        self.label_state_connect = Label(self,image=canvas2.entry_image_state_connect,bg="#FFFFFF")
        self.label_state_connect.place(x=688,y=41)

        canvas2.entry_image_time = PhotoImage(file=relative_to_assets("entry_time.png"))
        canvas2.create_image(165.0,35.0, image=canvas2.entry_image_time)

        self.second=StringVar()
        self.second.set("120")
    
        label_time = Label(
            self,
            anchor="center",
            font=("Montserrat Bold", 20 * -1),
            textvariable=self.second,
            bg="#5E95FF",  
            fg="#FFFFFF"
        )
        label_time.place(x=479, y=35)


        canvas3 = Canvas(
            self,
            bg="#FFFFFF",
            height=470,
            width=470,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas3.place(x=334, y=108)

        canvas3.entry_image_junction = PhotoImage(file=relative_to_assets("4way0degree.png"))

        self.label_image_junction = Label(self,image=canvas3.entry_image_junction,bg="#FFFFFF",anchor='center')
        self.label_image_junction.place(x=569,y=346,anchor='center')

        # self.parent.handle_btn_press(self.parent.reservations_btn, "res")

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

    def change_img_bt(self,bt):
        
        if bt == 'auto':
            self.button_auto.configure(image=self.image_auto_on)
            self.button_auto.image = self.image_auto_on

            self.button_manual.configure(image=self.image_manual_off)
            self.button_manual.image = self.image_manual_off

            self.button_red.configure(image=self.image_red_off)
            self.button_red.image = self.image_red_off

            self.button_flashing.configure(image=self.image_flashing_off)
            self.button_flashing.image = self.image_flashing_off

        elif bt == 'manual':
            self.button_auto.configure(image=self.image_auto_off)
            self.button_auto.image = self.image_auto_off

            self.button_manual.configure(image=self.image_manual_on)
            self.button_manual.image = self.image_manual_on

            self.button_red.configure(image=self.image_red_off)
            self.button_red.image = self.image_red_off

            self.button_flashing.configure(image=self.image_flashing_off)
            self.button_flashing.image = self.image_flashing_off

        elif bt == 'red':
            self.button_auto.configure(image=self.image_auto_off)
            self.button_auto.image = self.image_auto_off

            self.button_manual.configure(image=self.image_manual_off)
            self.button_manual.image = self.image_manual_off

            self.button_red.configure(image=self.image_red_on)
            self.button_red.image = self.image_red_on

            self.button_flashing.configure(image=self.image_flashing_off)
            self.button_flashing.image = self.image_flashing_off

        elif bt == 'flashing':
            self.button_auto.configure(image=self.image_auto_off)
            self.button_auto.image = self.image_auto_off

            self.button_manual.configure(image=self.image_manual_off)
            self.button_manual.image = self.image_manual_off

            self.button_red.configure(image=self.image_red_off)
            self.button_red.image = self.image_red_off

            self.button_flashing.configure(image=self.image_flashing_on)
            self.button_flashing.image = self.image_flashing_on

       
    def my_time(self):
        time_string = time.strftime('%H:%M:%S') # time format 
        self.label_timer.config(text=time_string)
        self.label_timer.after(1000,self.my_time) # time delay of 1000 milliseconds 

       
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

    def countup(self):
        
        try:
            temp =  int(self.second.get())
        except:
            print("Please input the right value")
        while temp < 360:
     
            secs = temp
    
      
            self.second.set("{0:3d}".format(secs))
    
            self.update()
            time.sleep(1)

            # if (temp == 0):
            #     messagebox.showinfo("Time Countdown", "Time's up ")
            
            temp += 1



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
