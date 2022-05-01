from pathlib import Path

from tkinter import (
    Frame,
    Canvas,
    Entry,
    Label,
    StringVar,
    Text,
    Button,
    PhotoImage,
    messagebox,
)
# import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def setting_main():
    Setting_main()


class Setting_main(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
   
        canvas = Canvas(
                self,
                bg="#E0DADA",
                height=670,
                width=980,
                bd=0,
                highlightthickness=0,
                relief="ridge",
            )
        canvas.place(x=0, y=0)


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
        canvas1.create_image(330, 25.0, image=canvas1.entry_text, anchor="nw")

        canvas1.label_password = Label(
            canvas1,
            anchor="n",
            font=("Inter", 18 , "bold"),
            textvariable=self.parent.password,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        canvas1.label_password.place(x=520, y=55, anchor="center")

        canvas1.image_button_edit = PhotoImage(file=relative_to_assets("bt_edit.png"))
        canvas1.button_edit = Button(
            canvas1,
            image=canvas1.image_button_edit,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("edit_password"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas1.button_edit.place(x=760.0, y=25.0, anchor="nw")


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
        canvas2.create_image(330, 25.0, image=canvas2.entry_text, anchor="nw")

        canvas2.label_ip = Label(
            canvas2,
            anchor="n",
            font=("Inter", 18 , "bold"),
            textvariable=self.parent.ip,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        canvas2.label_ip.place(x=520, y=55, anchor="center")

        canvas2.image_button_edit = PhotoImage(file=relative_to_assets("bt_edit.png"))
        canvas2.button_edit = Button(
            canvas2,
            image=canvas2.image_button_edit,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("edit_ip"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas2.button_edit.place(x=760.0, y=25.0, anchor="nw")


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
        canvas3.create_image(330, 25.0, image=canvas3.entry_text, anchor="nw")

        canvas3.label_junction = Label(
            canvas3,
            anchor="n",
            font=("Inter", 18 , "bold"),
            textvariable=self.parent.junction,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        canvas3.label_junction.place(x=520, y=55, anchor="center")


        canvas3.image_button_edit = PhotoImage(file=relative_to_assets("bt_edit.png"))
        canvas3.button_edit = Button(
            canvas3,
            image=canvas3.image_button_edit,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("edit_junction"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas3.button_edit.place(x=760.0, y=25.0, anchor="nw")
