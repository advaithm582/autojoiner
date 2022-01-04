from tkinter import messagebox
import tkinter as tk
import time


OBJECT_ORIENTED = False


main_window = menu_bar = meeting_list_frame = None

tic = ptic = float(0)

lbl = None


lblv = False

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
    global lbl
    # messagebox.showinfo("EXTENSIONFATHER IS RUNNING", ("Extensionfather is "
    #     "running properly, as intended."))
    
    menu_bar.make_list_to_menu([
        ["Timer", [
                ["Start", lambda: start(), "<Control-t>", lambda event: start()],
                ["Display progress", lambda: dprog(), "<Control-p>", lambda event: dprog()],
                ["Stop", lambda: stop(), "<Control-c>", lambda event: stop()],
                ["Reset", lambda: reset(), "<Control-r>", lambda event: reset()],
                ["Toggle Panel", lambda: cl_panel(), "<Control-o>", lambda event: cl_panel()]
            ]
        ]
    ])

def start():
    global lbl
    global tic, lblv, ptic
    if ptic:
        tic = time.time() - (time.time()-ptic)
    else:
        tic = time.time()
    if not lbl:
        lbl = tk.Label(main_window, text="Starting", font=("Calibri", 20))
        lblv = True
    lbl.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
    iterator()

def iterator():
    global lbl, tic
    if tic:
        toc = time.time()
        secs = toc-tic
        secs_, mins = secs%60, secs//60
        fmt = "%02d:%02d" % (mins, secs_)
        if mins >= 60:
            mins, hrs = mins%60, mins//60
            fmt = "%02d:%02d:%02d" % (hrs, mins, secs_)
        lbl["text"] = fmt
        lbl.after(1000, iterator)
    else:
        toc = time.time()
        secs = toc-ptic
        secs_, mins = secs%60, secs//60
        fmt = "%02d:%02d" % (mins, secs_)
        if mins >= 60:
            mins, hrs = mins%60, mins//60
            fmt = "%02d:%02d:%02d" % (hrs, mins, secs_)
        lbl["text"] = f"Timer stopped\n{fmt}"

def reset():
    global lbl, ptic
    stop()
    ptic = float(0)
    lbl["text"] = "00:00"

def cl_panel():
    global lbl, lblv
    # lbl.destroy()
    if lblv:
        lbl.grid_forget()
        lblv=False
    else:
        lbl.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        lblv=True

def stop():
    global tic, ptic
    ptic = tic
    tic = float(0)

def dprog():
    if tic:
        toc = time.time()
        secs = toc-tic
        secs_, mins = secs%60, secs//60
        fmt = "%02d:%02d" % (mins, secs_)
        messagebox.showinfo("Timer", f"Time spent is {fmt}")
    else:
        messagebox.showinfo("Timer", "Start the timer first.")