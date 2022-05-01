import threading
import time
import tkinter as tk
from gui.main_window.main import mainWindow
import main_control as control

# Main window constructor
root = tk.Tk()  # Make temporary window for app to start
root.withdraw()  # WithDraw the window

if __name__ == "__main__":

    control.runThreading()

    mainWindow()

    root.mainloop()


