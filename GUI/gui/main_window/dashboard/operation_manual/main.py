from pathlib import Path

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
# import controller as db_controller
# import trafficLightController as TrafficLightController

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def operation_manual():
    OperationManual()


class OperationManual(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#FFFFFF")

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

        canvas.image_bt_navigate = PhotoImage(file=relative_to_assets("bt_navigate.png"))
        self.button_navigate = Button(
            self,
            image=canvas.image_bt_navigate,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("main"),
            relief="flat",
            bg="#FFFFFF"
        )
        self.button_navigate.place(x=15.0, y=15.0, anchor="nw")

        canvas.image_text_manual = PhotoImage(file=relative_to_assets("text_manual.png"))
        canvas.create_image(190.0, 26.0, image=canvas.image_text_manual, anchor="n")

        canvas.image_line = PhotoImage(file=relative_to_assets("line.png"))
        canvas.create_image(190.0, 90.0, image=canvas.image_line, anchor="n")


        self.manual_window = {
            "4way" : Manual4Way(self),
            "3way" : Manual3Way(self)
        }

        self.setManualType(self.parent.numberOfJunction)
        self.setBorder(self.parent.numberOfJunction,self.parent.current_phase)

        if self.parent.current_mode == "manual":
            self.disable(self.parent.numberOfJunction,False)
        else: 
            self.disable(self.parent.numberOfJunction,True)

    def setManualType(self, numberOfJunction):
        # Hide all screens
        for manual_window in self.manual_window.values():
            manual_window.place_forget()

        # Show the screen of the button pressed
        if numberOfJunction == 4:
            self.manual_window["4way"].place(x=0, y=100, width=380.0, height=570.0)
        if numberOfJunction == 3:
            self.manual_window["3way"].place(x=0, y=100, width=380.0, height=570.0)

    def setBorder(self,numberOfJunction,current_phase):
        if numberOfJunction == 4:
            self.manual_window["4way"].setBorder(current_phase)
        elif numberOfJunction == 3:
            self.manual_window["3way"].setBorder(current_phase)

    def disable(self,numberOfJunction,state):
        if numberOfJunction == 4:
            self.manual_window["4way"].disable(state)
        elif numberOfJunction == 3:
            self.manual_window["3way"].disable(state)

class Manual4Way(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.image_button_4_way_1 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_4_way_2 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_4_way_3 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_4_way_4 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_4_way_5 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_4_way_6 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_4_way_7 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_4_way_8 = PhotoImage(file=relative_to_assets("4way/4way1.png"))

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=570,
            width=380,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=0, y=0)

        button_4_way_1 = Button(
            canvas,
            image=self.image_button_4_way_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.setManualType(3),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_1.place(x=120.0, y=70.0, anchor="center")

        button_4_way_2 = Button(
            canvas,
            image=self.image_button_4_way_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setBorder(2),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_2.place(x=260.0, y=70.0, anchor="center")

        button_4_way_3 = Button(
            canvas,
            image=self.image_button_4_way_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setBorder(3),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_3.place(x=120.0, y=210.0, anchor="center")

        button_4_way_4 = Button(
            canvas,
            image=self.image_button_4_way_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setBorder(4),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_4.place(x=260.0, y=210.0, anchor="center")

        button_4_way_5 = Button(
            canvas,
            image=self.image_button_4_way_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setBorder(5),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_5.place(x=120.0, y=350.0, anchor="center")

        button_4_way_6 = Button(
            canvas,
            image=self.image_button_4_way_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setBorder(6),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_6.place(x=260.0, y=350.0, anchor="center")
        
        button_4_way_7 = Button(
            canvas,
            image=self.image_button_4_way_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setBorder(7),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_7.place(x=120.0, y=490.0, anchor="center")

        button_4_way_8 = Button(
            canvas,
            image=self.image_button_4_way_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.disable(True),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_8.place(x=260.0, y=490.0, anchor="center")

        self.button_4_way = [button_4_way_1,button_4_way_2,button_4_way_3,button_4_way_4,button_4_way_5,button_4_way_6,button_4_way_7,button_4_way_8]
    
    def disable(self,state):
        if state:
            for button in self.button_4_way:
                button["state"] = "disabled"
        else:
            for button in self.button_4_way:
                button["state"] = "normal"

    def setBorder(self,n):
        for i in range(len(self.button_4_way)):
            if i == n-1:
                self.button_4_way[i]["bd"] = 3
            else:
                self.button_4_way[i]["bd"] = 0


class Manual3Way(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.image_button_3_way_1 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_3_way_2 = PhotoImage(file=relative_to_assets("4way/4way1.png"))
        self.image_button_3_way_3 = PhotoImage(file=relative_to_assets("4way/4way1.png"))

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=570,
            width=380,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=0, y=0)

        button_3_way_1 = Button(
            canvas,
            image=self.image_button_3_way_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.setManualType(4),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_3_way_1.place(x=120.0, y=70.0, anchor="center")

        button_3_way_2 = Button(
            canvas,
            image=self.image_button_3_way_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.setBorder(2),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_3_way_2.place(x=260.0, y=70.0, anchor="center")

        button_3_way_3 = Button(
            canvas,
            image=self.image_button_3_way_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: setLight(),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_3_way_3.place(x=120.0, y=210.0, anchor="center")


        self.button_3_way = [button_3_way_1,button_3_way_2,button_3_way_3]
    
    def disable(self,state):
        if state:
            for button in self.button_3_way:
                button["state"] = "disabled"
        else:
            for button in self.button_3_way:
                button["state"] = "normal"

    def setBorder(self,n):
        for i in range(len(self.button_3_way)):
            if i == n-1:
                self.button_3_way[i]["bd"] = 3
            else:
                self.button_3_way[i]["bd"] = 0




def setLight():
    print("Set port 1 to red")
    # TrafficLightController.setLightOn(1,"r")






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