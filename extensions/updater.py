import subprocess
import sys
import threading
from tkinter import messagebox

import zoom_autojoiner_gui
from zoom_autojoiner_gui.extensions import ExtensionAPI

ext_api = ExtensionAPI(__name__, "Updater", ver="0.1.0")

def main():
    op = subprocess.getoutput("gh_update -u 11c-csproject -r autojoiner "
                              f"-cv {zoom_autojoiner_gui.__version__} "
                              "--update")
    #print(zoom_autojoiner_gui.__version__, op, sep="\n")
    if op:
        y = messagebox.askyesno("Update Available", "A new version is available."
                            "\nInstall?")
        if y:
            threading.Thread(target=lambda: subprocess.run(op)).start()
            ext_api.main_window.destroy()
            sys.exit()
