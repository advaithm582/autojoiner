# This file is part of Zoom Autojoiner GUI.

# Zoom Autojoiner GUI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Zoom Autojoiner GUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Zoom Autojoiner GUI.  If not, see <https://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import gc
import json

from zoom_autojoiner_gui.extensions import ExtensionAPI

ext_api = ExtensionAPI(__name__, "Extensionfather", ver="0.1.0")

def main():
    mnu = tk.Menu(ext_api.ext_menu, tearoff = "off")
    mnu.add_command(label="List All Extensions", command=list_extensions)
    mnu.add_command(label="Add Extensions", command=add_extensions)
    ext_api.register_menu(mnu)

def list_extensions():
    exts = [obj for obj in gc.get_objects() if isinstance(obj, ExtensionAPI)]
    ostr = "Installed Extensions: \n"
    for ext in exts:
        ostr += "* "+ext.ext_name+" "+ext.ext_ver+"\n"

    messagebox.showinfo("Extensions", ostr)

def add_extensions():
    exts = [obj for obj in gc.get_objects() if isinstance(obj, ExtensionAPI)]
    n_ext = simpledialog.askstring("Enter extension name",
                                   "Enter extension name")
    ext_names = [ext.ext_codename for ext in exts]+[n_ext]
    estr = json.dumps(ext_names)
    nfile = "[enabled]\nextensions="+estr
    with open("config/extensions.ini", "w") as f:
        f.write(nfile)

    messagebox.showinfo("Extension Added", "Extension Added")

    
