from pathlib import Path
import time

from tkinter import (
    Frame,
    Canvas,
    Entry,
    Label,
    Text,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
import controller as db_controller
import global_data as GlobalData

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def operation_main():
    OperationMain()


class OperationMain(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#FFFFFF")

        self.plan_name=StringVar()
        self.plan_name.set("ช่วงเช้า 6 - 8 โมง")

        self.image_auto_off = PhotoImage(file=relative_to_assets("bt_auto_off.png"))
        self.image_auto_on = PhotoImage(file=relative_to_assets("bt_auto_on.png"))
        self.image_manual_off = PhotoImage(file=relative_to_assets("bt_manual_off.png"))
        self.image_manual_on = PhotoImage(file=relative_to_assets("bt_manual_on.png"))
        self.image_red_off = PhotoImage(file=relative_to_assets("bt_red_off.png"))
        self.image_red_on = PhotoImage(file=relative_to_assets("bt_red_on.png"))
        self.image_flashing_off = PhotoImage(file=relative_to_assets("bt_flashing_off.png"))
        self.image_flashing_on = PhotoImage(file=relative_to_assets("bt_flashing_on.png"))

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=670,
            width=380,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=0, y=0)


        canvas.image_text_mode = PhotoImage(file=relative_to_assets("text_mode.png"))
        canvas.create_image(190.0, 30.0, image=canvas.image_text_mode, anchor="n")

        self.button_auto = Button(
            self,
            image=self.image_auto_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.onAuto(),
            relief="flat",
            bg="#FFFFFF"
        )
        self.button_auto.place(x=190.0, y=95.0, anchor="n")

        self.button_manual = Button(
            self,
            image=self.image_manual_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.onMaual(),
            relief="flat",
            bg="#FFFFFF"
        )
        self.button_manual.place(x=190.0, y=180.0, anchor="n")

        self.button_red = Button(
            self,
            image=self.image_red_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.onRed(),
            relief="flat",
            bg="#FFFFFF"
        )
        self.button_red.place(x=190.0, y=265.0, anchor="n")

        self.button_flashing = Button(
            self,
            image=self.image_flashing_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.onFlashing(),
            relief="flat",
            bg="#FFFFFF"
        )
        self.button_flashing.place(x=190.0, y=350.0, anchor="n")

        # canvas.image_bt_navigate = PhotoImage(file=relative_to_assets("bt_navigate.png"))
        # self.button_navigate = Button(
        #     self,
        #     image=canvas.image_bt_navigate,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: self.parent.navigate("manual"),
        #     relief="flat",
        #     bg="#FFFFFF"
        # )
        # self.button_navigate.place(x=295.0, y=177.0, anchor="nw")
        
        canvas.image_text_plan = PhotoImage(file=relative_to_assets("text_plan.png"))
        canvas.create_image(190.0, 435.0, image=canvas.image_text_plan, anchor="n")

        label_plan_name = Label(
            self,
            anchor="n",
            font=("Inter", 18 , "bold"),
            textvariable=self.plan_name,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        label_plan_name.place(x=190, y=505, anchor="center")

        canvas.image_text_nowtime = PhotoImage(file=relative_to_assets("text_nowtime.png"))
        canvas.create_image(190, 550.0, image=canvas.image_text_nowtime, anchor="n")

        self.label_timer = Label(
            self,
            anchor="n",
            font=("Inter", 18 ,"bold"),
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        self.label_timer.place(x=190, y=620, anchor="center")
        self.my_time()
        self.loop()

    def onAuto(self):
        GlobalData.updateCurrentMode('auto')
    def onMaual(self):
        GlobalData.updateCurrentMode('manual')
        self.parent.navigate("manual")   
    def onRed(self):
        GlobalData.updateCurrentMode('red')
    def onFlashing(self):
        GlobalData.updateCurrentMode('flashing')
  

    def my_time(self):
        time_string = time.strftime('%H : %M : %S') # time format 
        self.label_timer.config(text=time_string)
        self.label_timer.after(1000,self.my_time) # time delay of 1000 milliseconds 

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

    def setPlanName(self,new_name):
        self.plan_name.set(new_name)
        

    def loop(self):
        self.change_img_bt(GlobalData.current_mode)
        self.setPlanName(GlobalData.current_plan_name)
        self.label_timer.after(200,self.loop)
  