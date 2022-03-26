"""Scrollable Frame"""

import tkinter as tk

from zoom_autojoiner_gui.views import MeetingListFrame
from zoom_autojoiner_gui.constants import ICON_FILE
from zoom_autojoiner_gui.extensions import ExtensionAPI

ext_api = ExtensionAPI(__name__, "Meeting List", ver="0.1.0")

##main_window = menu_bar = meeting_list_frame = None
##
##def set_objects(main_window_=None, menu_bar_=None, meeting_list_frame_=None):
##    """set_objects
##
##    Set the objects from the Extensions API.
##
##    Args:
##        main_window (tk.Tk): The TK Main window.
##        menu_bar (tk.Menu): The TK menubar
##        meeting_list_frame (tk.Frame): The TK Frame.
##
##    Note:
##        Only menu bar permission needed
##    """
##    global main_window, menu_bar, meeting_list_frame
##    main_window = main_window_
##    menu_bar = menu_bar_
##    meeting_list_frame = meeting_list_frame_

class Example(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = MeetingListFrame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def launch_window():
    root=tk.Tk()
    root.title("Meeting List")
    try:
        root.iconbitmap(ICON_FILE)
    except:
        pass
    example = Example(root)
    example.pack(side="top", fill="both", expand=True)
    root.mainloop()


def main():
    # messagebox.showinfo("EXTENSIONFATHER IS RUNNING", ("Extensionfather is "
    #     "running properly, as intended."))
    # print("jjj")
    
    data = tk.Menu(ext_api.ext_menu, tearoff = "off")
    data.add_command(label="Meeting List", command=launch_window)
    ext_api.register_menu(data)

ext_api.add_event_listener("application_loaded", main)