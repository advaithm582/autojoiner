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

"""Configuration Constants

This file reads run-time config constants.
"""

import json
import logging
import configparser

logger = logging.getLogger(__name__)
try:
    logger.info("Attempting to load config...")
    # with open("config/config.json", "r") as cfg_file:
    #     cfg = json.loads(cfg_file.read())
    #     ICON_FILE = cfg["ICON_FILE"]
    #     DB_URL = cfg["DB_URL"]
    #     PYAG_PICS_DIR = cfg["PYAG_PICS_DIR"]
    #     MY_NAME = cfg["MY_NAME"]
    #     THEME_FILE = "themes/" + cfg["THEME_FILE"]

    # Parse the config file.
    config = configparser.ConfigParser()
    

    # read it
    config.read("config/application.ini")
    # Tkinter configuration
    ICON_FILE = config["tkinter"]["icon"]
    THEME_FILE = "themes/" + config["tkinter"]["theme"] + ".thm.json"

    # Database configuration
    DB_URL = config["database"]["uri"]

    # Autojoiner configuration
    PYAG_PICS_DIR = config["autojoiner"]["pictures_dir"]
    MY_NAME = config["autojoiner"]["name"]

    """The Extensions Config Variable"""
    EXTENSIONS = config["extensions"]
    
except Exception as e:
    logger.error("Failed to load config, exiting...", exc_info=True)
    exit(1)
else:
    logger.info("Config loaded.")
