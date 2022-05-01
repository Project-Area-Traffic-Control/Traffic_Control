from logging import disable
from pathlib import Path
import controller as db_controller
import api_controller as api

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
from tkinter.ttk import Treeview

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def edit_junction():
    Edit_junction()


class Edit_junction(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.junctionDataList = []
        self.junctionList = []

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

        canvas.image_edit_ip = PhotoImage(file=relative_to_assets("text_edit_junction.png"))
        canvas.create_image(50, 66.0, image=canvas.image_edit_ip, anchor="w")


        # JunctionList(self).place(x=309, y=35, width=611.0, height=60.0, anchor="nw")
        

        canvas.image_bt_cancel = PhotoImage(file=relative_to_assets("bt_cancel.png"))
        canvas.bt_cancel = Button(
            canvas,
            image=canvas.image_bt_cancel,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate('main'),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas.bt_cancel.place(x=490.0, y=585.0, anchor="n")

    def loadData(self):
        self.junctionDataList = []

        result = api.getAllJunction()
        
        for item in result:

            junction = {
                'id': item['id'],
                'name': item['name'],
                'number_channel': item['number_channel'],
                'rotate': item['rotate']
            }
            self.junctionDataList.append(junction)

        self.placeJunctionList()

    def placeJunctionList(self):
        n = 0
        for junctionData in self.junctionDataList:
            if n < 6:
                Junction = JunctionList(self)
                Junction.setData(junctionData)
                Junction.place(x=309, y=35+(60*n)+(25*n), width=611.0, height=60.0, anchor="nw")
                n += 1
  
class JunctionList(Frame):
    def __init__(self, parent,controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
      
        self.junctionData = {}

        self.name_junction = StringVar()

        canvas = Canvas(
                self,
                bg="#FFFFFF",
                height=60,
                width=611,
                bd=0,
                highlightthickness=0,
                relief="ridge",
            )
        canvas.place(x=0, y=0)

        canvas.entry_text = PhotoImage(file=relative_to_assets("entry_text.png"))
        canvas.create_image(0, 0, image=canvas.entry_text, anchor="nw")

        canvas.label_junction = Label(
            canvas,
            anchor="n",
            font=("Inter", 18 , "bold"),
            textvariable=self.name_junction,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        canvas.label_junction.place(x=190, y=30, anchor="center")

        canvas.image_bt_select = PhotoImage(file=relative_to_assets("bt_select.png"))
        canvas.bt_select = Button(
            canvas,
            image=canvas.image_bt_select,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.saveJunction(),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas.bt_select.place(x=611.0, y=0.0, anchor="ne")

    def setData(self,data):
        self.junctionData = {
            'id': data['id'],
            'name': data['name'],
            'number_channel': data['number_channel'],
            'rotate': data['rotate']
        }
        self.loadName()

    def loadName(self):
        self.name_junction.set(self.junctionData['name'])

    def saveJunction(self):
        # print('Save ',self.junctionData['name'])
        db_controller.updateJunction(self.junctionData)
        self.parent.parent.navigate('main')

    # def Select(self):
        
