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


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def junction_image():
    JunctionImage()


class JunctionImage(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg="#FFFFFF")
        self.temp_phase = -1
        self.temp_rotate = -1

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=575,
            width=575,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.place(x=0, y=0)

        self.image_junction_3way_defult = PhotoImage(file=relative_to_assets("3way/0/3way_defult.png"))


        self.label_image_junction = Label(canvas,image=self.image_junction_3way_defult,bg="#FFFFFF")
        self.label_image_junction.place(x=287.5,y=287.5,anchor='center')


        self.chanel_n = StringVar()
        self.chanel_e = StringVar()
        self.chanel_s = StringVar()
        self.chanel_w = StringVar()

        label_chanel_n = Label(
            canvas,
            anchor="n",
            font=("Inter", 16 , "bold"),
            textvariable=self.chanel_n,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        label_chanel_n.place(x=285, y=30, anchor="nw")

        label_chanel_e = Label(
            canvas,
            anchor="n",
            font=("Inter", 16 , "bold"),
            textvariable=self.chanel_e,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        label_chanel_e.place(x=390, y=385, anchor="nw")

        label_chanel_s = Label(
            canvas,
            anchor="n",
            font=("Inter", 16 , "bold"),
            textvariable=self.chanel_s,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        label_chanel_s.place(x=207, y=515, anchor="nw")

        label_chanel_w = Label(
            canvas,
            anchor="n",
            font=("Inter", 16 , "bold"),
            textvariable=self.chanel_w,
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )
        label_chanel_w.place(x=180, y=160, anchor="ne")
      
        self.loop()


    def changChangeImagePhase(self,phase_number,rotate):
        junction = GlobalData.junction
        number_channel = junction['number_channel']
        if number_channel == 3:
            if phase_number < 5:
                image_junction = PhotoImage(file=relative_to_assets(f"3way/{rotate}/3way_{phase_number}.png"))
                self.label_image_junction.configure(image=image_junction)
                self.label_image_junction.image = image_junction

            if GlobalData.current_mode == 'red' or GlobalData.current_mode == 'flashing':
                image_junction = PhotoImage(file=relative_to_assets(f"3way/{rotate}/3way_defult.png"))
                self.label_image_junction.configure(image=image_junction)
                self.label_image_junction.image = image_junction

        elif number_channel == 4:
            global pathImg
            if rotate == 0:
              pathImg = f"4way/4way_{phase_number}.png"
            elif rotate == 90:
                if phase_number < 5:
                    pathImg = f"4way/4way_{(phase_number%4)+1}.png"
                elif phase_number == 5:
                    pathImg = f"4way/4way_6.png"
                elif phase_number == 6:
                    pathImg = f"4way/4way_5.png"
                elif phase_number == 7:
                    pathImg = f"4way/4way_8.png"
                elif phase_number == 8:
                    pathImg = f"4way/4way_7.png"

            elif rotate == 180:
                if phase_number == 1:
                    pathImg = f"4way/4way_3.png"
                elif phase_number == 2:
                    pathImg = f"4way/4way_4.png"
                elif phase_number == 3:
                    pathImg = f"4way/4way_1.png"
                elif phase_number == 4:
                    pathImg = f"4way/4way_2.png"
                else:
                    pathImg = f"4way/4way_{phase_number}.png"
            elif rotate == 270:
                if phase_number == 1:
                    pathImg = f"4way/4way_4.png"
                elif phase_number == 2:
                    pathImg = f"4way/4way_1.png"
                elif phase_number == 3:
                    pathImg = f"4way/4way_2.png"
                elif phase_number == 4:
                    pathImg = f"4way/4way_3.png"
                elif phase_number == 5:
                    pathImg = f"4way/4way_6.png"
                elif phase_number == 6:
                    pathImg = f"4way/4way_5.png"
                elif phase_number == 7:
                    pathImg = f"4way/4way_8.png"
                elif phase_number == 8:
                    pathImg = f"4way/4way_7.png"

            image_junction = PhotoImage(file=relative_to_assets(pathImg))
            self.label_image_junction.configure(image=image_junction)
            self.label_image_junction.image = image_junction

            if GlobalData.current_mode == 'red' or GlobalData.current_mode == 'flashing':
                image_junction = PhotoImage(file=relative_to_assets(f"4way/4way_defult.png"))
                self.label_image_junction.configure(image=image_junction)
                self.label_image_junction.image = image_junction
    
        
    def setText(self,):
        junction = GlobalData.junction
        channel = GlobalData.channel
        rotate = junction['rotate']
        number_channel = junction['number_channel']
        if rotate == 0:
            for ch in channel:
                if ch['order_number'] == 1:
                    self.chanel_n.set(ch['name'])
                elif ch['order_number'] == 2:
                    self.chanel_e.set(ch['name'])
                elif ch['order_number'] == 3:
                    self.chanel_w.set(ch['name'])
                elif ch['order_number'] == 4:
                    self.chanel_s.set(ch['name'])

            if number_channel == 3:
                    self.chanel_s.set('')

        elif rotate == 90:
            for ch in channel:
                if ch['order_number'] == 1:
                    self.chanel_e.set(ch['name'])
                elif ch['order_number'] == 2:
                    self.chanel_s.set(ch['name'])
                elif ch['order_number'] == 3:
                    self.chanel_n.set(ch['name'])
                elif ch['order_number'] == 4:
                    self.chanel_w.set(ch['name'])

            if number_channel == 3:
                self.chanel_w.set('')

        elif rotate == 180:
            for ch in channel:
                if ch['order_number'] == 1:
                    self.chanel_s.set(ch['name'])
                elif ch['order_number'] == 2:
                    self.chanel_w.set(ch['name'])
                elif ch['order_number'] == 3:
                    self.chanel_e.set(ch['name'])
                elif ch['order_number'] == 4:
                    self.chanel_n.set(ch['name'])

            if number_channel == 3:
                self.chanel_n.set('')

        elif rotate == 270:
            for ch in channel:
                if ch['order_number'] == 1:
                    self.chanel_w.set(ch['name'])
                elif ch['order_number'] == 2:
                    self.chanel_n.set(ch['name'])
                elif ch['order_number'] == 3:
                    self.chanel_s.set(ch['name'])
                elif ch['order_number'] == 4:
                    self.chanel_e.set(ch['name'])

            if number_channel == 3:
                self.chanel_e.set('')

    def loop(self):

        current_phase = GlobalData.current_phase
        rotate = GlobalData.junction['rotate']

        if GlobalData.phase_changed:
            self.changChangeImagePhase(current_phase,rotate)

        if self.temp_rotate != rotate:
            self.setText()

        self.tempPhase = current_phase
        self.temp_rotate = rotate
        self.label_image_junction.after(200,self.loop)