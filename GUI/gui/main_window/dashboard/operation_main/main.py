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

        canvas.image_bt_navigate = PhotoImage(file=relative_to_assets("bt_navigate.png"))
        self.button_navigate = Button(
            self,
            image=canvas.image_bt_navigate,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("manual"),
            relief="flat",
            bg="#FFFFFF"
        )
        self.button_navigate.place(x=295.0, y=177.0, anchor="nw")
        
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
   
    #     self.data = {
    #         "id": StringVar(),
    #         "meal": StringVar(),
    #         "type": StringVar(),
    #         "g_id": StringVar(),
    #         "check_in": StringVar(),
    #         "room_id": StringVar(),
    #         "reservation_date": StringVar(),
    #         "check_out": StringVar(),
    #     }

    #     self.initialize()

    #     self.canvas = Canvas(
    #         self,
    #         bg="#FFFFFF",
    #         height=432,
    #         width=797,
    #         bd=0,
    #         highlightthickness=0,
    #         relief="ridge",
    #     )

    #     self.canvas.place(x=0, y=0)
    #     self.canvas.create_rectangle(
    #         40.0, 14.0, 742.0, 16.0, fill="#EFEFEF", outline=""
    #     )

    #     self.canvas.create_text(
    #         116.0,
    #         33.0,
    #         anchor="nw",
    #         text="Update Reservation",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 26 * -1),
    #     )

    #     self.canvas.create_text(
    #         116.0,
    #         65.0,
    #         anchor="nw",
    #         text="Change Details",
    #         fill="#808080",
    #         font=("Montserrat SemiBold", 16 * -1),
    #     )

    #     self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    #     button_1 = Button(
    #         self,
    #         image=self.button_image_1,
    #         borderwidth=0,
    #         highlightthickness=0,
    #         command=lambda: self.parent.navigate("add"),
    #         relief="flat",
    #     )
    #     button_1.place(x=40.0, y=33.0, width=53.0, height=53.0)

    #     self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    #     image_1 = self.canvas.create_image(145.0, 150.0, image=self.image_image_1)

    #     self.canvas.create_text(
    #         60.0,
    #         125.0,
    #         anchor="nw",
    #         text="Reservation ID",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 14 * -1),
    #     )

    #     self.id_text = self.canvas.create_text(
    #         60.0,
    #         152.0,
    #         anchor="nw",
    #         text="Select record first...",
    #         fill="#979797",
    #         font=("Montserrat Bold", 18 * -1),
    #     )

    #     self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    #     image_2 = self.canvas.create_image(145.0, 246.0, image=self.image_image_2)

    #     self.canvas.create_text(
    #         60.0,
    #         221.0,
    #         anchor="nw",
    #         text="Is Taking Meal",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 14 * -1),
    #     )

    #     self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    #     entry_bg_1 = self.canvas.create_image(149.5, 258.0, image=self.entry_image_1)
    #     entry_2 = Entry(
    #         self,
    #         bd=0,
    #         bg="#EFEFEF",
    #         highlightthickness=0,
    #         font=("Montserrat Bold", 18 * -1),
    #         foreground="#777777",
    #         textvariable=self.data["meal"],
    #     )
    #     entry_2.place(x=60.0, y=246.0, width=179.0, height=22.0)

    #     self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    #     image_3 = self.canvas.create_image(145.0, 342.0, image=self.image_image_3)

    #     self.canvas.create_text(
    #         60.0,
    #         317.0,
    #         anchor="nw",
    #         text="Type",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 14 * -1),
    #     )

    #     self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    #     entry_bg_2 = self.canvas.create_image(149.5, 354.0, image=self.entry_image_2)
    #     entry_3 = Entry(
    #         self,
    #         bd=0,
    #         bg="#EFEFEF",
    #         highlightthickness=0,
    #         font=("Montserrat Bold", 18 * -1),
    #         foreground="#777777",
    #         textvariable=self.data["type"],
    #     )
    #     entry_3.place(x=60.0, y=342.0, width=179.0, height=22.0)

    #     self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
    #     image_4 = self.canvas.create_image(391.0, 150.0, image=self.image_image_4)

    #     self.canvas.create_text(
    #         306.0,
    #         125.0,
    #         anchor="nw",
    #         text="Guest Id",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 14 * -1),
    #     )

    #     self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_2.png"))
    #     entry_bg_3 = self.canvas.create_image(395.5, 162.0, image=self.entry_image_3)
    #     entry_4 = Entry(
    #         self,
    #         bd=0,
    #         bg="#EFEFEF",
    #         highlightthickness=0,
    #         font=("Montserrat Bold", 18 * -1),
    #         foreground="#777777",
    #         textvariable=self.data["g_id"],
    #     )
    #     entry_4.place(x=306.0, y=150.0, width=179.0, height=22.0)

    #     self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
    #     image_5 = self.canvas.create_image(391.0, 246.0, image=self.image_image_5)

    #     self.canvas.create_text(
    #         306.0,
    #         221.0,
    #         anchor="nw",
    #         text="Check-in Time",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 14 * -1),
    #     )

    #     self.entry_image_4 = PhotoImage(file=relative_to_assets("entry_2.png"))
    #     entry_bg_4 = self.canvas.create_image(395.5, 258.0, image=self.entry_image_4)
    #     entry_5 = Entry(
    #         self,
    #         bd=0,
    #         bg="#EFEFEF",
    #         highlightthickness=0,
    #         font=("Montserrat Bold", 18 * -1),
    #         foreground="#777777",
    #         textvariable=self.data["check_in"],
    #     )
    #     entry_5.place(x=306.0, y=246.0, width=179.0, height=22.0)

    #     self.image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
    #     image_6 = self.canvas.create_image(391.0, 342.0, image=self.image_image_6)

    #     self.canvas.create_text(
    #         306.0,
    #         317.0,
    #         anchor="nw",
    #         text="Reservation Date",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 14 * -1),
    #     )

    #     self.entry_image_5 = PhotoImage(file=relative_to_assets("entry_2.png"))
    #     entry_bg_5 = self.canvas.create_image(395.5, 354.0, image=self.entry_image_5)
    #     entry_6 = Entry(
    #         self,
    #         bd=0,
    #         bg="#EFEFEF",
    #         highlightthickness=0,
    #         font=("Montserrat Bold", 18 * -1),
    #         foreground="#777777",
    #         textvariable=self.data["reservation_date"],
    #     )
    #     entry_6.place(x=306.0, y=342.0, width=179.0, height=22.0)

    #     self.image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
    #     image_7 = self.canvas.create_image(637.0, 150.0, image=self.image_image_7)

    #     self.canvas.create_text(
    #         552.0,
    #         125.0,
    #         anchor="nw",
    #         text="Room Id",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 14 * -1),
    #     )

    #     self.entry_image_6 = PhotoImage(file=relative_to_assets("entry_2.png"))
    #     entry_bg_6 = self.canvas.create_image(641.5, 162.0, image=self.entry_image_6)
    #     entry_7 = Entry(
    #         self,
    #         bd=0,
    #         bg="#EFEFEF",
    #         highlightthickness=0,
    #         font=("Montserrat Bold", 18 * -1),
    #         foreground="#777777",
    #         textvariable=self.data["room_id"],
    #     )
    #     entry_7.place(x=552.0, y=150.0, width=179.0, height=22.0)

    #     self.image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
    #     image_8 = self.canvas.create_image(637.0, 246.0, image=self.image_image_8)

    #     self.canvas.create_text(
    #         552.0,
    #         221.0,
    #         anchor="nw",
    #         text="Check Out Time",
    #         fill="#5E95FF",
    #         font=("Montserrat Bold", 14 * -1),
    #     )

    #     self.entry_image_7 = PhotoImage(file=relative_to_assets("entry_2.png"))
    #     entry_bg_7 = self.canvas.create_image(641.5, 258.0, image=self.entry_image_7)
    #     entry_8 = Entry(
    #         self,
    #         bd=0,
    #         bg="#EFEFEF",
    #         highlightthickness=0,
    #         font=("Montserrat Bold", 18 * -1),
    #         foreground="#777777",
    #         textvariable=self.data["check_out"],
    #     )
    #     entry_8.place(x=552.0, y=246.0, width=179.0, height=22.0)

    #     self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    #     button_2 = Button(
    #         self,
    #         image=self.button_image_2,
    #         borderwidth=0,
    #         highlightthickness=0,
    #         command=self.handle_update,
    #         relief="flat",
    #     )
    #     button_2.place(x=570.0, y=318.0, width=144.0, height=48.0)

    # def initialize(self):
    #     self.selected_r_id = self.parent.selected_rid
    #     self.reservation_data = self.parent.reservation_data

    #     # Filter out all reservations for selected id reservation
    #     self.selected_reservation_data = list(
    #         filter(lambda x: str(x[0]) == self.selected_r_id, self.reservation_data)
    #     )

    #     if self.selected_reservation_data:
    #         self.selected_reservation_data = self.selected_reservation_data[0]

    #         self.canvas.itemconfigure(
    #             self.id_text, text=self.selected_reservation_data[0]
    #         )
    #         self.data["g_id"].set(self.selected_reservation_data[1])
    #         self.data["room_id"].set(self.selected_reservation_data[2])
    #         self.data["check_in"].set(self.selected_reservation_data[3])
    #         self.data["check_out"].set(self.selected_reservation_data[4])
    #         self.data["meal"].set(self.selected_reservation_data[5])
    #         self.data["reservation_date"].set(self.selected_reservation_data[3])

    # def handle_update(self):

    #     data = [
    #         x
    #         for x in [
    #             self.data[label].get()
    #             for label in ("g_id", "check_in", "room_id", "check_out", "meal")
    #         ]
    #     ]

    #     # Update data and show alert
    #     if db_controller.update_reservation(self.selected_r_id, *data):
    #         messagebox.showinfo("Success", "Reservation Updated Successfully")
    #         self.parent.navigate("view")

    #         self.reset()

    #     else:
    #         messagebox.showerror(
    #             "Error", "Error Updating Reservation. Please check all ids exist"
    #         )

    #     self.parent.refresh_entries()
    # def reset(self):
    #     # clear all entries
    #     for label in self.data:
    #         self.data[label].set("")

    #     self.canvas.itemconfigure(
    #         self.id_text, text="Select source first..."
    #     )
