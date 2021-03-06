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
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def edit_password():
    Edit_password()


class Edit_password(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.new_password=StringVar()

        self.configure(bg="#FFFFFF")

        canvas = Canvas(
                self,
                bg="#FFFFFF",
                height=670,
                width=980,
                bd=0,
                highlightthickness=0,
                relief="ridge",
            )
        canvas.place(x=0, y=0)

        canvas.image_edit_password = PhotoImage(file=relative_to_assets("text_edit_password.png"))
        canvas.create_image(50, 66.0, image=canvas.image_edit_password, anchor="w")

        canvas.entry_text = PhotoImage(file=relative_to_assets("entry_text.png"))
        canvas.create_image(490, 66.0, image=canvas.entry_text, anchor="center")

        canvas.label_password = Label(
            canvas,
            anchor="n",
            font=("Inter", 18 , "bold"),
            textvariable=self.new_password,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        canvas.label_password.place(x=490, y=66, anchor="center")

        canvas_numpad = Canvas(
                self,
                bg="#FFFFFF",
                height=400,
                width=295,
                bd=0,
                highlightthickness=0,
                relief="ridge",
            )
        canvas_numpad.place(x=490, y=335,anchor="center")

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



        canvas.image_save = PhotoImage(file=relative_to_assets("bt_save.png"))
        canvas.button_save = Button(
            canvas,
            image=canvas.image_save,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.save_password(),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas.button_save.place(x=307.0, y=574.0, anchor="nw")

        canvas.image_cancel = PhotoImage(file=relative_to_assets("bt_cancel.png"))
        canvas.button_cancel = Button(
            canvas,
            image=canvas.image_cancel,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("main"),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas.button_cancel.place(x=502.0, y=574.0, anchor="nw")



    def on_press_number(self,value):
        if value != 'del':
            self.new_password.set(self.new_password.get()+value)
        else:
            self.new_password.set(self.new_password.get()[:-1])
            
    def reset_new_value(self):
        self.new_password.set(self.parent.password.get())

    def save_password(self):
        if self.new_password.get() != "":
            db_controller.updatePassword(self.new_password.get())
            self.parent.password.set(self.new_password.get())
            self.parent.navigate("main")