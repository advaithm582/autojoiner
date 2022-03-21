import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json
import datetime

from zoom_autojoiner_gui.constants import DB_URL
from zoom_autojoiner_gui.controllers import DatabaseHandler


OBJECT_ORIENTED = False


main_window = menu_bar = meeting_list_frame = None

def set_objects(main_window_=None, menu_bar_=None, meeting_list_frame_=None):
    """set_objects

    Set the objects from the Extensions API.

    Args:
        main_window (tk.Tk): The TK Main window.
        menu_bar (tk.Menu): The TK menubar
        meeting_list_frame (tk.Frame): The TK Frame.
    """
    global main_window, menu_bar, meeting_list_frame
    main_window = main_window_
    menu_bar = menu_bar_
    meeting_list_frame = meeting_list_frame_

def main():
    global menu_bar, dbh
    # messagebox.showinfo("EXTENSIONFATHER IS RUNNING", ("Extensionfather is "
    #     "running properly, as intended."))
    # print("jjj")
    
    data = tk.Menu(menu_bar, tearoff = "off")
    data.add_command(label="Clear", command=clear_data)
    data.add_command(label="Refresh", command=refresh_data)
    data.add_command(label="Export", command=export_data)
    data.add_command(label="Import (no overwrite)", command=import_data)
    data.add_command(label="Import (overwrite)", command=overwrite_data)
    menu_bar.add_cascade(label="Data", menu=data)
    dbh = DatabaseHandler(DB_URL)
    
def clear_data():
    yes = messagebox.askyesno("Delete Data?", "This action is irreversible.\nContinue?")
    if yes:
        dbh.truncate_table()
        meeting_list_frame.reload_table()
        messagebox.showinfo("Success", "Data Deleted")

def refresh_data():
    meeting_list_frame.reload_table()
    
def export_data():
    filename = filedialog.asksaveasfilename(defaultextension='.json',
                filetypes=(
                    ("JSON files", "*.json"),
                    ("All files", "*.*"),
                ))
    try:
        with open(filename, "w") as fh:
            ddump = [{
                    "id" : record["id"],
                    "mtg_provider" : record["mtg_provider"], 
                    "mtg_id" : record["mtg_id"], 
                    "mtg_password" : record["mtg_password"],
                    "mtg_time": record["mtg_time"].strftime("%Y-%m-%d %H:%M:%S") 
                } for record in dbh.get_mtg_data_to_list()]
            json.dump(ddump, fh)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    else:
        messagebox.showinfo("Success", "Data Exported")
        
def import_data():
    filename = filedialog.askopenfilename(filetypes=(
                    ("JSON files", "*.json"),
                    ("All files", "*.*"),
                ))
    try:
        with open(filename, "r") as fh:
            mtgdata_ = json.load(fh)
            mtgdata = [{
                    "id" : record["id"],
                    "mtg_provider" : record["mtg_provider"], 
                    "mtg_id" : record["mtg_id"], 
                    "mtg_password" : record["mtg_password"],
                    "mtg_time": datetime.datetime.strptime(record["mtg_time"], "%Y-%m-%d %H:%M:%S") 
                } for record in mtgdata_]
            for mtg in mtgdata:
                dbh.add_mtg(mtg["mtg_id"], mtg["mtg_password"], mtg["mtg_time"], mtg["mtg_provider"])
    except Exception as e:
        messagebox.showerror("Error", str(e))
    else:
        messagebox.showinfo("Success", "Data Imported")
        refresh_data()
        
def overwrite_data():
    clear_data()
    import_data()