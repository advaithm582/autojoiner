import sys
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

from zoom_autojoiner_gui.constants import ICON_FILE
from zoom_autojoiner_gui.extensions import ExtensionAPI


ext_api = ExtensionAPI(__name__, "Debugging Tools", ver="0.1.0")

def main():
    mnu = tk.Menu(ext_api.ext_menu, tearoff = "off")
    mnu.add_command(label="Standard Output (stdout)", command=stdout_view)
    mnu.add_command(label="Standard Error (stderr)", command=stderr_view)
    mnu.add_command(label="Code Runner Interface", command=coderunner_view)
    mnu.add_command(label="Execute single line of code using exec", command=exec_code_single)
    mnu.add_command(label="Execute single line of code using eval", command=eval_code)
    ext_api.register_menu(mnu)

class StdoutRedirector(object):
    # https://stackoverflow.com/questions/18517084/how-to-redirect-stdout-to-a-tkinter-text-widget
    
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(self):
        pass


class StdoutViewerInterface(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        # self.title("Debugging Window")
        try:
            self.iconbitmap(ICON_FILE)
        except:
            pass

        self.text_box = tk.Text(self, wrap='word', height = 11,
                                width=50)
        self.text_box.grid(column=0, row=0, columnspan = 2,
                           sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)


class CoderunnerInterface(tk.Tk):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self.title("Run Code")
        try:
            self.iconbitmap(ICON_FILE)
        except:
            pass

        self.prevcode = tk.Text(self, wrap='word', height = 11,
                                width=50)
        self.prevcode.grid(column=0, row=0, columnspan = 2,
                           sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

        # To Execute CODE (tecode)
        self.tecode = tk.Text(self, wrap='word', height = 5,
                                width=30)
        self.tecode.grid(column=0, row=1,
                         sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

        self.execute = ttk.Button(self, text="Execute", command=self.exc_code)
        self.execute.grid(column=1, row=1,
                          sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)

    def exc_code(self):
        code = self.tecode.get("1.0", "end-1c")
        exec(code)
        self.prevcode.insert("end", code)
        self.prevcode.insert("end", "\n")
        self.prevcode.see("end")
        self.tecode.delete('1.0', tk.END)
        

def stdout_view():
    swi = StdoutViewerInterface()
    swi.title("Standard Output")
    sys.stdout = StdoutRedirector(swi.text_box)
    swi.mainloop()


def stderr_view():
    swi = StdoutViewerInterface()
    swi.title("Standard Error")
    sys.stderr = StdoutRedirector(swi.text_box)
    swi.mainloop()    


def coderunner_view():
    cri = CoderunnerInterface()
    cri.mainloop()


def exec_code_single():
    exec(simpledialog.askstring("Enter code",
                                   "Enter code:"))


def eval_code():
    eval(simpledialog.askstring("Enter code",
                                   "Enter single line of code:"))
