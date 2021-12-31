import os
import traceback
import threading, time
from datetime import datetime
from ctypes import windll
from PIL import ImageGrab

def internal_save_screenshot():
    """internal_save_screenshot [summary]

    Returns:
        [type]: [description]
    """
    try:
        img = ImageGrab.grabclipboard()
        if img:
            file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
            print(f"{file_name} is the file name")
            path = os.path.join(c['save_dir'], file_name)
            # Save the image to disk
            img.save(path, 'PNG')
            # img.save('paste.jpg', 'JPEG')
            return True
        else:
            return False
    except Exception as e:
        print("An error occured.", e)
        print(traceback.format_exc())

def save_screenshot():
    if internal_save_screenshot():
        print("Success!")
        return True
    else:
        print("Error")


class AutoCopyThread(threading.Thread):
    def __init__(self, *a, **kw):
        super().__init__(*a, daemon = True, **kw)
        self.warning = False
        self.do_run = False

    def run(self):
        # while self.inc <= 14400:
        while True:
            while self.do_run:
                if not self.warning: 
                    print("AUTOSAVE RUNNING!!!")
                    self.warning = True

                if internal_save_screenshot():
                    print("Success! \a")
                    if windll.user32.OpenClipboard(None):
                        windll.user32.EmptyClipboard()
                        windll.user32.CloseClipboard()

                time.sleep(0.5)

            self.warning = False
            time.sleep(0.5)


class ForegroundThread(threading.Thread):
    def __init__(self, bg_thread:AutoCopyThread, *a, **kw):
        """__init__ [summary]

        Args:
            bg_thread (AutoCopyThread): [description]
        """
        self.bg_thread = bg_thread
        super().__init__(*a, **kw)
        

    def run(self):
        print(MANUAL)
        while True:
            prompt = input("Enter a command: ").lower()

            if prompt == "save" or prompt == "s":
                save_screenshot()
            elif prompt == "exit" or prompt == "quit" or prompt == "q":
                self.bg_thread.do_run = False
                # self.bg_thread.join()
                exit()
            elif prompt == "en2s":
                c['en2s'] = "0" if c['en2s']=="1" else "1"
                print(f"Enter to save has been toggled to {c['en2s']}")
                cfg_obj.save_changes()
            elif prompt.strip() == "" and c['en2s'] == "1":
                save_screenshot()
            elif prompt == "h":
                print(MANUAL)
            elif prompt == "stats":
                print("Parent DIR = %s\nEnter to save = %s" % (c['save_dir'], c['en2s']))
            elif prompt == "autosave":
                self.bg_thread.do_run = False if self.bg_thread.do_run else True
                print(self.bg_thread.do_run, "is the status")
                # self.bg_thread.run()
            else:
                print("Enter a valid command.")

bg_thread = AutoCopyThread()
bg_thread.start()

main_thread = ForegroundThread(bg_thread)
main_thread.start()