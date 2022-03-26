import subprocess
import threading
import os
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import pyautogui

from zoom_autojoiner_gui.constants import PYAG_PICS_DIR, DB_URL
from zoom_autojoiner_gui.controllers import DatabaseHandler
from zoom_autojoiner_gui.extensions import ExtensionAPI

ext_api = ExtensionAPI(__name__, "Google Meet Autojoiner Tool", ver="0.1.1")

def autojoiner_cb(mtid, mtpw=None):
    # Start Edge
    pf86 = subprocess.getoutput("echo %PROGRAMFILES(x86)%")
    threading.Thread(target=lambda: subprocess.call([pf86
                     +r'\Microsoft\Edge\Application\msedge.exe',
                     "--app=https://meet.google.com/"+mtid])).start()

    # f to get picture dir
    # pic = lambda p: os.path.join(PYAG_PICS_DIR, "GMEET", p)

    # pyautogui.write("https://meet.google.com/"+mtid, interval=0.1)
    # pyautogui.press('enter')

class NewGoogleMeetingDialog(tk.Toplevel):
    def __init__(self, tk_frame_handle = None, tk_root_element = None):
        """This class shows the New Meeting Dialog box."""
        # DB handle
        self.__dbh = DatabaseHandler(DB_URL)

        # TK Root Element
        if tk_root_element:
            # Attach it to var
            self.tk_root_element = tk_root_element
        else:
            # Get Root element from frame
            self.tk_root_element = None

        # Toplevel Initialization
        try:
            # print("HI")
            super().__init__(self.tk_root_element)
        except:
            super().__init__()

        # TK Frame
        if tk_frame_handle:
            # If given use it
            self.tk_frame_handle = tk_frame_handle
        elif self.tk_root_element:
            # Take from root element
            self.tk_frame_handle = self.tk_root_element.__meeting_list_frame
        else:
            # None it
            self.tk_frame_handle = None

        #setting title
        self.title("New Google Meet Meeting")
        #setting window size
        width=338
        height=200
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        # For modal dialog
        self.grab_set()
        try:
            # if platform.system() == "Windows": self.attributes('-toolwindow', True)
            self.transient(self.tk_root_element)
            # self.attributes('-topmost', True)
        except:
            pass

        # Meeting Time Label
        self.GLabel_3=ttk.Label(self)
        self.GLabel_3["text"] = "Mtg. Time"
        self.GLabel_3.place(x=0,y=40,width=101,height=30)

        # Title Label
        self.GLabel_276=ttk.Label(self)
        self.GLabel_276["justify"] = "center"
        self.GLabel_276["text"] = "New Google Meet Meeting"
        self.GLabel_276.place(x=0,y=0,width=350,height=30)

        # Meeting Time Entry
        self.DateTimeEntry=ttk.Entry(self)
        self.DateTimeEntry.place(x=110,y=40,width=220,height=30)

        # Meeting ID label
        self.GLabel_378=ttk.Label(self)
        # ft = tkFont.Font(family='Times',size=10)
        self.GLabel_378["text"] = "Code"
        self.GLabel_378.place(x=0,y=80,width=100,height=30)

        # Meeting ID entry
        self.MeetingIDEntry=ttk.Entry(self)
        self.MeetingIDEntry.place(x=110,y=80,width=220,height=30)

        # Meeting Passcode Label
        self.GLabel_48=ttk.Label(self)
        self.GLabel_48["text"] = "GMeetings are not passcode-protected"
        # self.GLabel_48.place(x=0,y=120,width=101,height=30)
        self.GLabel_48.place(x=0,y=120,height=30)

        # Meeting Password Entry
        # self.MeetingPasscodeEntry=ttk.Entry(self)
        # self.MeetingPasscodeEntry.place(x=110,y=120,width=220,height=30)

        # Create Meeting Button
        self.CreateMtgButton=ttk.Button(self)
        # CreateMtgButton["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Times',size=10)
        # CreateMtgButton["font"] = ft
        # CreateMtgButton["fg"] = "#000000"
        # CreateMtgButton["justify"] = "center"
        self.CreateMtgButton["text"] = "Create"
        self.CreateMtgButton.place(x=260,y=160,width=70,height=35)
        self.CreateMtgButton["command"] = self.CreateMtgButton_command

        # Cancel New Meeting Button
        self.CancelButton=ttk.Button(self)
        # CancelButton["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Times',size=10)
        # CancelButton["font"] = ft
        # CancelButton["fg"] = "#000000"
        # CancelButton["justify"] = "center"
        self.CancelButton["text"] = "Cancel"
        self.CancelButton.place(x=170,y=160,width=70,height=35)
        self.CancelButton["command"] = self.CancelButton_command

    def CreateMtgButton_command(self):
        try:
            datetimeobj=datetime.datetime.strptime(self.DateTimeEntry.get(), "%Y-%m-%d %H:%M:%S")
            self.__dbh.add_mtg(self.MeetingIDEntry.get(),
                               "", datetimeobj, "GMEET")
        except Exception as e:
            messagebox.showerror("Error", "An exception has occured.\nError Details:\n%s" % (str(e)))
        else:
            messagebox.showinfo("Information", "Meeting Added.")
            try:
                self.tk_frame_handle.reload_table()
            except:
                messagebox.showinfo("Information", "Failed to refresh table data. Please refresh manually.")
            self.destroy()
            

    def CancelButton_command(self):
        self.destroy()


def add_mtg():
    NewGoogleMeetingDialog(ext_api.meeting_list_frame,
                           ext_api.main_window)
    

def main():
    mnu = tk.Menu(tearoff = "off")
    mnu.add_command(label="Add Google Meet Meeting", command=add_mtg)
    # mnu.add_command(label="Add Extensions", command=add_extensions)
    ext_api.register_menu(mnu)
    ext_api.register_autojoiner_callback(mtg_provider="GMEET",
                                     callback=autojoiner_cb)

ext_api.add_event_listener("application_loaded", main)