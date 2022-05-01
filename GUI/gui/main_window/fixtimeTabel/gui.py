from ast import Lambda
import datetime
from distutils.command.config import config
from itertools import starmap
from pathlib import Path
from sqlite3 import Date
import time
from tkinter.constants import ANCHOR, N
from tkinter.tix import ButtonBox
from tkinter.ttk import Style, Treeview
from turtle import left, right
from gui.main_window.dashboard.junction_image.main import JunctionImage
# from matplotlib.figure import Figure
from gui.main_window.dashboard.operation_main.main import OperationMain
from gui.main_window.dashboard.operation_manual.main import OperationManual
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import BOTH, BOTTOM, HORIZONTAL, LEFT, RIGHT, VERTICAL, Y, Button, Frame, Canvas, Entry, Label, PhotoImage, N, Scrollbar, StringVar, messagebox
from tkinter import *
import controller as db_controller
import api_controller as api
import global_data as GlobalData
import main_control as control


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def fixtimeTabel():
    FixtimeTabel()


class FixtimeTabel(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.plans_data = []


        self.configure(bg="#E0DADA")

        canvas = Canvas(
                self,
                bg="#FFFFFF",
                height=670,
                width=980,
                bd=0,
                highlightthickness=0,
                relief="ridge",
            )
        canvas.place(x=25, y=25)

        canvas.image_text_tabel = PhotoImage(file=relative_to_assets("text_tabel_plan.png"))
        canvas.create_image(25, 55.0, image=canvas.image_text_tabel, anchor="w")

        canvas.image_bt_load_data = PhotoImage(file=relative_to_assets("bt_load_data.png"))
        canvas.bt_load_data = Button(
            canvas,
            image=canvas.image_bt_load_data,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.loadData(),
            relief="flat",
            bg="#FFFFFF"
        )
        canvas.bt_load_data.place(x=955.0, y=55.0, anchor="e")


        canvas1 = Canvas(
                self,
                bg="#FFFFFF",
                width=930,
                height=535,
                bd=0,
                highlightthickness=0,
                relief="ridge",
                scrollregion=(0,0,535,930)
            )
        canvas1.place(x=50.0, y=135, anchor="nw")

        self.loop_label = Label(
            canvas,
            anchor="n",
            font=("Inter", 16 , "bold"),
            bg="#FFFFFF",  
            fg="#4F4F4F"
        )

        style = Style()
       
        
        style.theme_use("default")
        style.map("Treeview")
        style.configure("Treeview.Heading", font=('Inter', 16, 'bold') ,  bg="#FFFFFF",  fg="#4F4F4F" )
        style.configure('Treeview', rowheight=40, font=('Inter', 14) )

        
      
        self.tv = Treeview(canvas1, show='headings', selectmode="none")
        self.tv.place(x=465.0, y=0,height=535, anchor="n")

        self.tv['columns'] = ('no','start', 'stop', 'plan')

        sb = Scrollbar(self, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)

        self.tv.config(yscrollcommand=sb.set)
        sb.config(command=self.tv.yview)

       

        self.tv.column("#0", width=0,  stretch=NO)
        self.tv.column("no",anchor=CENTER, width=90)
        self.tv.column("start",anchor=CENTER, width=280)
        self.tv.column("stop",anchor=CENTER,width=280)
        self.tv.column("plan",anchor=CENTER,width=280)

        self.tv.heading("#0",text="",anchor=CENTER)
        self.tv.heading("no",text="ลำดับ",anchor=CENTER)
        self.tv.heading("start",text="เวลาเริ่มต้น",anchor=CENTER)
        self.tv.heading("stop",text="เวลาสิ้นสุด",anchor=CENTER)
        self.tv.heading("plan",text="เเผนการทำงาน",anchor=CENTER)

        self.loadDataToDB(False)
        self.setDataToTabel()

        self.loop()
        


    def loop(self):
        self.setDataToTabel()
        self.loop_label.after(1000,self.loop)

    def loadData(self):
        status = self.loadDataToDB(True)
        if status:
            control.stop()
            control.runThreading()
            
    def updateDataPlans(self):
        GlobalData.plans_data = db_controller.getPlans()
            
    def setDataToTabel(self):
        data = GlobalData.plans_data
        self.deleteTabel()
        n=0
        select = []
        for item in data:

            start = item['start']
            end = item['end']
            now = datetime.datetime.now()
            t1 = now.replace(hour=0,minute=0,second=0,microsecond=0)
            t2 = now.replace(hour=0,minute=0,second=59,microsecond=999999)
            start = t1 + start
            end = t2 + end

            row = self.tv.insert(parent='',index='end',iid=n,text='',
            values=(n+1,start.strftime('%H : %M'),end.strftime('%H : %M'),item['name']))
            
            if start.time() < now.time() and now.time() < end.time():
                select.append(row)

            n += 1
        self.tv.selection_set(select)


    def deleteTabel(self):
        for row in self.tv.get_children():
            self.tv.delete(row)

    def loadDataToDB(self,showErr):
        junctionData = db_controller.getJunction()
        result = api.getFixtimeTabel(junctionData['id'])
        if result:
            db_controller.deleteAllPlan()
            db_controller.deleteAllPattern()
            n = 0
            for item in result:
                start = api.convertDataTimeToLocal(item['start'])
                end = api.convertDataTimeToLocal(item['end'])
                data = {
                    'id': n,
                    'start': start.time().replace(second=0),
                    'end': end.time().replace(second=0),
                    'name': item['plan']['name'],
                    'yellow_time': item['plan']['yellow_time'],
                    'delay_red_time': item['plan']['delay_red_time'],
                    'plan_id': item['plan']['id'],
                }
                db_controller.addPlan(data)

                patterns = api.getPlanByID(data['plan_id'])['pattern']
                for pattern in patterns:
                    dataPattern = {
                        "plan_id": n,
                        "pattern": pattern['pattern'],
                        "order": pattern['order'],
                        "duration": pattern['duration']
                    }
                    db_controller.addPattern(dataPattern)

                n += 1

           
            self.loadChanelToDB()
            self.loadJunctionDataToDB()
            self.updateDataPlans()
            self.loadDataToGlobal()

            if showErr:
                messagebox.showinfo(
                        message=f"โหลดข้อมูลสำเร็จ",
                    )

            return True

        elif showErr:
            messagebox.showerror(
                    message=f"ไม่สามารถโหลดข้อมูลได้ กรุณาลองใหม่อีกครั้ง",
                )
            return False
        else:
            return False

   
    def loadChanelToDB(self):
        junctionData = GlobalData.junction
        result = api.getChannels(junctionData['id'])
        db_controller.deleteAllChannel()
        for item in result:
            global port_forward
            global port_right
            port_forward = 0
            port_right = 0

            for phase in item['phase']:
     

                if phase['type'] == 'FORWARD':
                    port_forward = phase['port_number']
                elif phase['type'] == 'TURN_RIGHT':
                    port_right = phase['port_number']

            data = {
                "order_number": item['order'],
                "name":  item['name'],
                "port_forward": port_forward,
                "port_right": port_right
            }
            db_controller.addChannel(data)

    def loadDataToGlobal(self):
        GlobalData.updateJunction()
        GlobalData.updateChannel()

    def loadJunctionDataToDB(self):
      
        new_junction = api.getJunctionByID(GlobalData.junction['id'])
        data = self.junctionData = {
            'id': new_junction['id'],
            'name': new_junction['name'],
            'number_channel': new_junction['number_channel'],
            'rotate': new_junction['rotate']
        }
    
        db_controller.updateJunction(data)
