from pathlib import Path

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

        self.temp_numberOfJunction = -1
        self.temp_phase = -1
        self.temp_mode = -1
        self.temp_rotate = -1

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

        self.label_loop = Label(canvas,bg="#FFFFFF")

        self.manual_window = {
            "4way" : Manual4Way(self),
            "3way" : Manual3Way(self)
        }

        self.loop()
        

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

    def changeImgageRotate(self,numberOfJunction):
        if numberOfJunction == 3:
            self.manual_window["3way"].changImgage()
        elif numberOfJunction == 4:
            self.manual_window["4way"].changImgage()

    def loop(self):
        junction = GlobalData.junction
        current_phase = GlobalData.current_phase
        current_mode = GlobalData.current_mode
        number_channel = junction['number_channel']

        if self.temp_numberOfJunction != number_channel:
            GlobalData.current_phase = 1
            self.setManualType(number_channel)
            self.changeImgageRotate(number_channel)
            

        if self.temp_rotate != junction['rotate']:
            self.changeImgageRotate(number_channel)
      
        if self.temp_mode != current_mode:
            if current_mode == "manual":
                self.disable(number_channel,False)
            else: 
                self.disable(number_channel,True)

        if GlobalData.phase_changed:
            self.setBorder(number_channel,current_phase)
            
        self.temp_numberOfJunction = number_channel
        self.temp_rotate = junction['rotate']
        self.temp_phase = current_phase
        self.temp_mode = current_mode

        self.label_loop.after(200,self.loop)

class Manual4Way(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

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
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(1),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_1.place(x=120.0, y=70.0, anchor="center")

        button_4_way_2 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(2),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_2.place(x=260.0, y=70.0, anchor="center")

        button_4_way_3 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(3),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_3.place(x=120.0, y=210.0, anchor="center")

        button_4_way_4 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(4),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_4.place(x=260.0, y=210.0, anchor="center")

        button_4_way_5 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(5),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_5.place(x=120.0, y=350.0, anchor="center")

        button_4_way_6 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(6),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_6.place(x=260.0, y=350.0, anchor="center")
        
        button_4_way_7 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(7),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_7.place(x=120.0, y=490.0, anchor="center")

        button_4_way_8 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(8),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_4_way_8.place(x=260.0, y=490.0, anchor="center")

        self.button_4_way = [button_4_way_1,button_4_way_2,button_4_way_3,button_4_way_4,button_4_way_5,button_4_way_6,button_4_way_7,button_4_way_8]
    
    

    def changePhase(self,phase):
        GlobalData.phase_changed = False
        GlobalData.updateCurrentPhase(phase)
        
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
    
    
    def changImgage(self):
        result = GlobalData.junction
        rotate = result['rotate']
        global pathImg 

        n = 1
        for button in self.button_4_way:
            if rotate == 0:
              pathImg = f"4way/4way_{n}.png"
            elif rotate == 90:
                if n < 5:
                    pathImg = f"4way/4way_{(n%4)+1}.png"
                elif n == 5:
                    pathImg = f"4way/4way_6.png"
                elif n == 6:
                    pathImg = f"4way/4way_5.png"
                elif n == 7:
                    pathImg = f"4way/4way_8.png"
                elif n == 8:
                    pathImg = f"4way/4way_7.png"

            elif rotate == 180:
                if n == 1:
                    pathImg = f"4way/4way_3.png"
                elif n == 2:
                    pathImg = f"4way/4way_4.png"
                elif n == 3:
                    pathImg = f"4way/4way_1.png"
                elif n == 4:
                    pathImg = f"4way/4way_2.png"
                else:
                    pathImg = f"4way/4way_{n}.png"
            elif rotate == 270:
                if n == 1:
                    pathImg = f"4way/4way_4.png"
                elif n == 2:
                    pathImg = f"4way/4way_1.png"
                elif n == 3:
                    pathImg = f"4way/4way_2.png"
                elif n == 4:
                    pathImg = f"4way/4way_3.png"
                elif n == 5:
                    pathImg = f"4way/4way_6.png"
                elif n == 6:
                    pathImg = f"4way/4way_5.png"
                elif n == 7:
                    pathImg = f"4way/4way_8.png"
                elif n == 8:
                    pathImg = f"4way/4way_7.png"



            image_bt = PhotoImage(file=relative_to_assets(pathImg))
            button.configure(image=image_bt)
            button.image = image_bt
            n += 1


class Manual3Way(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

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
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(1),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_3_way_1.place(x=120.0, y=70.0, anchor="center")

        button_3_way_2 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(2),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_3_way_2.place(x=260.0, y=70.0, anchor="center")

        button_3_way_3 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(3),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_3_way_3.place(x=120.0, y=210.0, anchor="center")

        button_3_way_4 = Button(
            canvas,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changePhase(4),
            relief="solid",
            bg="#FFFFFF", 
            bd=0
        )
        button_3_way_4.place(x=260.0, y=210.0, anchor="center")


        self.button_3_way = [button_3_way_1,button_3_way_2,button_3_way_3,button_3_way_4]

    def changePhase(self,phase):
        GlobalData.phase_changed = False
        GlobalData.updateCurrentPhase(phase)
    
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

    def changImgage(self):
        result = GlobalData.junction
        rotate = result['rotate']

        n = 1
        for button in self.button_3_way:
            image_bt = PhotoImage(file=relative_to_assets(f"3way/{rotate}/3way_{n}.png"))
            button.configure(image=image_bt)
            button.image = image_bt
            n += 1


