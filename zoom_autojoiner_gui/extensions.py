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

import typing as t
import logging
import sys
import os
import json
import tkinter as tk
from importlib import import_module
from configparser import ConfigParser

# from zoom_autojoiner_gui.views import (
#     MainWindow,
#     ApplicationMenuBar,
#     MeetingListFrame
# )
from zoom_autojoiner_gui.constants import EXTENSIONS
from zoom_autojoiner_gui.views import Autojoiner


logger = logging.getLogger(__name__) # This creates logger for this file.


#: bool : Whether extension API is enabled or not.
enabled = EXTENSIONS.getboolean("enabled")


class NoSuchEventError(Exception):
    def __init__(self, evt):
        super().__init__("There is no such event for which handlers "
                         "can be registered - " + evt)


class NoEventHandlerError(Exception):
    def __init__(self, evt):
        super().__init__("There is no event handler for the event " + evt)


class ExtensionHandler():
    """ExtensionHandler
    
    This class deals with the handling of ZAJ
    Python Extensions. 

    Args:
        config: The Extensions Config dict.

    Returns:
        NoneType
    """
    
    #: tuple : The tuple of permissions.
    permissions = (
        "main_window",
        "menu_bar",
        "meeting_list_frame"
    )

    def __init__(self, config: ConfigParser) -> None:
        self.basic_config = config
        self.config = ConfigParser()

        # real_path = os.path.realpath(__file__)
        # dir_path = os.path.dirname(real_path)
        dir_path = '' # not package path -- makes more sense
        
        logger.debug("DIR path %s" % dir_path)

        # Extension configuration
        self.config.read(os.path.join(dir_path, "config", 
            self.basic_config['config'] + '.ini'))

        # Extension DIR
        
        self.extensions_dir = os.path.join(dir_path, self.basic_config['dir'])

        self.extensions = {}

        logger.debug(os.path.join(dir_path, "config", 
            self.basic_config['config'] + '.ini'))

    def get_ext(self) -> list:
        """get_ext

        Gets the enabled extensions from
        the extension configuration file.

        Returns:
            The list of enabled extensions.
        """
        return json.loads(self.config['enabled']['extensions'])

    def get_extension_permission(self, ext_name: str, 
            permission_name: str) -> bool:
        """get_extension_permissions

        Get the permission for an extension.

        Args:
            ext_name: The name of an extension.
            permission_name: The name of a permission to check.

        Returns:
            A boolean value. 
            If the permission is granted, it returns True. Or else it 
            returns False.
        """
        return self.config.getboolean(ext_name, permission_name, 
            fallback=False)

    def load_extensions(self) -> bool:
        """load_extensions

        Load all the extensions.

        Returns:
            True if everything went fine
            False if even one extension failed

        Note:
            If one extension failed, others are still executed.
            Like a parallel circuit, if one bulb fuses others don't.
        """
        all_ext_ran = True

        # sys.path.insert(0, self.extensions_dir)
        sys.path.append(self.extensions_dir) # can't override builtins

        for extension in self.get_ext():
            try:
                self.extensions[extension] = import_module(extension)
            except:
                logger.error(f"Failed to load extension {extension}!",
                    exc_info=True)
                all_ext_ran = False

        return all_ext_ran

    def give_extensions_prefs(self) -> bool:
        """give_extensions_prefs

        Give extensions their preferences. This is stored in the same 
        section where their permissions are stored. The preferences are
        passed to a function in the extension, `get_prefs` where they
        are given the ConfigParser Object of their section in an argument
        `prefs_dict`.

        Returns:
            True if everything went fine
            False if even one extension failed

        Note:
            An extension should have implemented the module level function
            `get_prefs` in order for this to work.
            If one extension failed, others are still executed.
            Like a parallel circuit, if one bulb fuses others don't.
        """
        all_ext_ran = True

        for extension in self.get_ext():
            try:
                self.extensions[extension].get_prefs(prefs_dict=self.config[extension])
            except:
                logger.error(f"Failed to give obj to ext {extension}!",
                    exc_info=True)
                all_ext_ran = False

        return all_ext_ran

    def give_extensions_objects(self, main_window: tk.Tk = None, 
            menu_bar: tk.Menu = None, 
            meeting_list_frame: tk.Frame = None) -> bool:
        """give_extensions_objects

        Give extensions the currently used Tkinter objects. It also depends
        on the permissions granted to the extensions. For example, if an 
        extension was not given meeting_list_frame permission, then a None
        object will be passed to it instead.

        Args:
            main_window: The Main window of the ZAJ.
            menu_bar: Application menu Bar
            meeting_list_frame: Meeting lsit frame object.

        Returns:
            True if everything went fine
            False if even one extension failed

        Note:
            An extension should have implemented the module level function
            `set_objects` in order for this to work.
            If one extension failed, others are still executed.
            Like a parallel circuit, if one bulb fuses others don't.
        """

        # Whether all extensions ran successfully
        all_ext_ran = True

        for extension in self.extensions:
            try:
                objects = {}
                for permission in self.permissions:
                    if self.get_extension_permission(extension, permission):
                        objects[permission] = locals()[permission]
                        # logger.debug(f"{objects}, {locals()}")
                    else:
                        objects[permission] = None
                self.extensions[extension].set_objects(
                        objects["main_window"],
                        objects["menu_bar"],
                        objects["meeting_list_frame"]
                    )
                logger.debug(f"EXT_NAME{extension}\nOBJECTS:{objects}")
            except:
                logger.error(f"Failed to set extension {extension}!", 
                    exc_info=True)
                all_ext_ran = False

        return all_ext_ran

    def run_extensions(self) -> bool:
        """run_extensions

        Run all the extensions.

        Returns:
            True if everything went fine
            False if even one extension failed

        Note:
            If one extension failed, others are still executed.
            Like a parallel circuit, if one bulb fuses others don't.
        """

        all_ext_ran = True

        for extension in self.extensions:
            try:
                self.extensions[extension].main()
            except:
                logger.error(f"Failed to run extension {extension}!", 
                    exc_info=True)
                all_ext_ran = False

        return all_ext_ran


class ExtensionAPI():
    """ExtensionAPI
    
    The Extension API object can be used for:
    1. Adding new Autojoiners
    2. Registering Menus

    Args:
        codename: Codename
        name (str): Name of the extension
        ver: Version string of extension.
    """
    ext_menu = None
    main_window = None
    menu_bar = None
    meeting_list_frame = None

    #: list: Menus to be registered
    reg_menus = []

    #: tuple: Available event listeners
    event_listeners = (
        "test", # test
        "application_loaded", # Completed application loading
        "add_meeting", # Add Meeting 
        "edit_meeting", # Edit a Meeting (arg: Record ID)
        "join_meeting", # Join a meeting
        "no_autojoiner_callback_error", # no callback registered
        )
    
    #: dict: Registered event listeners
    reg_eventlisteners = {k: [] for k in event_listeners}
    
    def __init__(self, codename: str, name: str, ver: str = "1.0") -> None:
        self.ext_codename = codename
        self.ext_name = name
        self.ext_ver = ver

    def register_menu(self, menu: tk.Menu) -> None:
        """register_menu 
        
        Register an autojoiner menu. This will appear under a dropdown
        'Extensions' in the menubar, with a further dropdown entry, 
        with the name of the extension as a label.
        
        Note:
            The menus will be stored in a queue. Registration is 
            performed only once the core application is initialised.

        Args:
            menu (tk.Menu): The Menu object.
        """
        self.reg_menus.append((self.ext_name, menu))

    def register_autojoiner_callback(self, mtg_provider: str,
                                     callback: t.Callable) -> None:
        """register_autojoiner_callback 
        
        Register an autojoiner callback

        Args:
            mtg_provider (str): 
                The Meeting provider. N.B. ZM cannot be overrided as
                of now.
            callback (t.Callable): The Callback
        """
        # self.reg_autojoiners[mtg_provider] = callback
        Autojoiner.register_autojoiner(mtg_provider, callback)
        
    def add_event_listener(self, event: str, 
                           callback: t.Callable) -> None:
        """add_event_listener 
        
        Register an event listener

        Args:
            event (str): 
                The Event.
            callback (t.Callable): The Callback
        """
        event_hdlrs = self.reg_eventlisteners.get(event)
        
        if event not in self.event_listeners or event_hdlrs == None:
            raise NoSuchEventError(event)
        else:
            event_hdlrs.append(callback)
    
    @classmethod
    def event_occured(cls, event: str, onlydefault: bool = False, 
                      args: list = [], kwds: dict = {}) -> None:
        """event_occured 
        
        Call the event listeners for an event.

        Args:
            event (str): The Event name
            onlydefault (bool, optional): 
                Call only the first event listener. Defaults to False.
            args (list, optional): 
                Positional arguments to pass to the event listener. 
                Defaults to [].
            kwds (dict, optional): 
                Keyword arguments to pass to the event listener. 
                Defaults to {}.
        """
        event_hdlrs = cls.reg_eventlisteners.get(event)
        
        if event not in cls.event_listeners or event_hdlrs == None:
            raise NoSuchEventError(event)
        else:
            if onlydefault:
                if len(event_hdlrs) == 0:
                    raise NoEventHandlerError(event)
                else:
                    event_hdlrs[0].__call__(*args, **kwds)
            else:
                for func in event_hdlrs:
                    func.__call__(*args, **kwds)

    @classmethod
    def set_ext_menu(cls, menu: tk.Menu) -> None:
        """set_ext_menu 
        
        Internal method - Used to set the menu for the `register_menu`
        command.
        
        DO NOT CALL THIS METHOD FROM YOUR EXTENSION.

        Args:
            menu (tk.Menu): _description_
        """
        cls.ext_menu = menu

    @classmethod
    def internal_tkreg_menus(cls) -> None:
        """internal_tkreg_menus

        Internally used to register method with Tk Menu.
        
        DO NOT CALL THIS METHOD FROM YOUR EXTENSION.
        """
        for label, menu in cls.reg_menus:
            cls.ext_menu.add_cascade(label=label, menu=menu)

    @classmethod
    def internal_set_tkobj(cls, main_window: tk.Tk = None, 
            menu_bar: tk.Menu = None, 
            meeting_list_frame: tk.Frame = None) -> None:
        """internal_set_tkobj 
        
        Internal method to set the TK Objects. These are forwarded to 
        attributes
        
        DO NOT CALL THIS METHOD FROM YOUR EXTENSION.

        Args:
            main_window (tk.Tk, optional): 
                The Main Window object. Defaults to None.
            menu_bar (tk.Menu, optional): 
                The Menubar. Defaults to None.
            meeting_list_frame (tk.Frame, optional): 
                Meeting List Frame. Defaults to None.
        """
        cls.main_window = main_window
        cls.menu_bar = menu_bar
        cls.meeting_list_frame = meeting_list_frame


def load_extensions():
    if EXTENSIONS.getboolean("enabled"):
        # if extensions are enabled
        global ext_class
        ext_class = ExtensionHandler(EXTENSIONS)
        if ext_class.load_extensions():
            ext_class.run_extensions()
