import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


import chevron

def _(text):
    return text

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Zoom Autojoiner Configuration Tool")
        
        self.w_title = tk.Label(self, text="Zoom Autojoiner Configuration Tool")
        self.w_title.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
        # Theme
        
        self.w_theme_lbl = tk.Label(self, text="Theme")
        self.w_theme_lbl.grid(row=1, column=0, sticky=tk.N+tk.S+tk.W, padx=5, pady=5)
        
        self.w_theme_text = tk.StringVar()
        self.w_theme_options = ["Dark", "Light"]
        self.w_theme_optn = ttk.OptionMenu(self, self.w_theme_text, 
                                           "--select--", *self.w_theme_options)
        self.w_theme_optn.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
        # Name
        
        self.w_name_lbl = tk.Label(self, text="Your name")
        self.w_name_lbl.grid(row=2, column=0, sticky=tk.N+tk.S+tk.W, padx=5, pady=5)
        
        self.w_name_optn = ttk.Entry(self)
        self.w_name_optn.grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
        # directory
        
        self.w_pdir_lbl = tk.Label(self, text="Pictures directory")
        self.w_pdir_lbl.grid(row=3, column=0, sticky=tk.N+tk.S+tk.W, padx=5, pady=5)
        
        self.w_pdir_btn = ttk.Button(self, text="Browse...", command=lambda: self.w_pdir_callback())
        self.w_pdir_btn.grid(row=3, column=1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
        # extn
        
        self.w_extension_status = tk.IntVar()
        self.w_extension_cb = ttk.Checkbutton(self, text='Enable Extensions API',
                                             variable=self.w_extension_status, onvalue=1, offvalue=0)
        self.w_extension_cb.grid(row=4, column=0, columnspan=2,
                                 sticky=tk.N+tk.S+tk.W, padx=5, pady=5)
        
        # update
        
        self.w_update_btn = ttk.Button(self, text="Apply Preferences", command=lambda: self.update_cfg())
        self.w_update_btn.grid(row=5, column=0, columnspan=2,
                               sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        self.w_cancel_btn = ttk.Button(self, text="Cancel", command=lambda: self.destroy())
        self.w_cancel_btn.grid(row=6, column=0, columnspan=2,
                               sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
    def w_pdir_callback(self):
        self.w_pdir_dir = filedialog.askdirectory()
        self.w_pdir_btn["text"] = self.w_pdir_dir
        
    def update_cfg(self):
        if len(sys.argv)>1 and os.path.isdir(sys.argv[1]):
            messagebox.showinfo("Application Reconfiguration Information", 
                                "It appears that the configuration"
                                " tool was launched by the installer. You "
                                "can also run the configuration tool anytime"
                                " by navigating to: \n"
                                f"{sys.argv[1]}\\ConfigTool.exe\n")
            path = sys.argv[1]
        else:
            path = "config/"
            
        data = {
            "please_dont_modify_file": "You can modify this file.",
            "theme": self.w_theme_text.get().lower(),
            "user_name": self.w_name_optn.get(),
            "pictures_dir": self.w_pdir_dir,
            "use_extensions": "true" if self.w_extension_status.get()
                                        else "false"
        }
        
        try:
            config_final = open(os.path.join(path, "application.ini"), "w")
            template = open(os.path.join(path, "application-default.ini.mustache"), "r")
            config_final.write(chevron.render(template, data))
            config_final.close()
            template.close()
        except:
            messagebox.showerror("Failed to update configuration",
                                 "The tool failed to update the configuration.")
        else:
            messagebox.showinfo("Success", "Configuration Updated.")
            self.destroy()


if __name__=="__main__":
    a = MainWindow()
    a.mainloop()
