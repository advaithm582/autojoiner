import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox

import zoom_autojoiner_gui
from zoom_autojoiner_gui.extensions import ExtensionAPI

ext_api = ExtensionAPI(__name__, "Updater", ver="0.2.0")

def splash_window():
    win = tk.Tk()
    win.title("Please wait...")
    win.overrideredirect(True)
    win.geometry("400x200")
    win.eval('tk::PlaceWindow . center')
    win.attributes('-topmost', True)
    win.update()
    tk.Label(win, text= "Please Wait...", fg= "black",
        font=('serif', 40, "bold")).pack(pady=20)
    tk.Label(win, text= "Zoom Autojoiner GUI Update is downloading", fg= "black",
        font=('serif', 15)).pack(pady=20)
    return win

def main():
    gupd = subprocess.getoutput("gh_update -u 11c-csproject -r autojoiner "
                              f"-cv {zoom_autojoiner_gui.__version__} "
                              "--check-latest")
    #print(zoom_autojoiner_gui.__version__, op, sep="\n")
    if gupd=="False":
        # Not the latest version
        y = messagebox.askyesno("Update Available", "A new version is "
                                "available. \nDownload and Install?")
        if y:
            ext_api.main_window.destroy()
            # spwin = splash_window()
            op = subprocess.getoutput("gh_update -u 11c-csproject "
                                      "-r autojoiner -cv "
                                      f"{zoom_autojoiner_gui.__version__} "
                                      "--update --fixed-filename")
            # threading.Thread(target=lambda: subprocess.run(op)).start()
            # spwin.destroy()
            subprocess.Popen([op])
            sys.exit()


ext_api.add_event_listener("application_loaded", main)
