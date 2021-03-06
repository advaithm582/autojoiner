# Zoom Autojoiner

This program is to aid in automatically joining Zoom Meetings.

### ⚠️ WARNING ⚠️: This Program is no longer maintained. Use at your own risk. 
### The archive of installers can be found here: [ZOHO WORKDRIVE](https://workdrive.zohopublic.in/folder/gc2944a6c06e96e4543f3b55066196a4bd566), latest version `0.4.3`

## Goals:
* To serve as a meeting notice board
* To remind that it is time to join a meeting
* To aid in typing long meeting IDs and passcodes

## Use Scenario:
You are working on an assignment, and you are so focused that you forget that your meeting is now. When you realise that you had the meeting, you open Whatsapp Web to get the passcode and ID. It takes 10 minutes to load, only to show you that it can't connect to the phone. Now you scramble about for your cell phone. You are furious as Fingerprint Unlock fails. Finally, you copy the Meeting ID to the Zoom interface, enter the passcode wrongly once, and join the meeting. Once you join, you realise that you have joined in your mother's account.

Now you come to GitHub, and find this diamond in the ocean of gems. You just add your meeting in the intutive interface and BAM! When it is time, you will find your cursor automatically moving, and you will now remember about the meeting, and you can get ready while we do the clicking for you!

## What **not** to use this program for:
* Overloading Zoom Servers with Join Meeting requests
* Attending your classes on your behalf
* Other uses that do not fit in to the goals of this program

# User Manual
## Installation and Configuration
### Configuring constants in `config.json`
```
{
	"ICON_FILE" : "ZoomAJIcon.ico",
	"PYAG_PICS_DIR" : "",
	"DB_URL" : "sqlite:///database.db",
	"THEME_FILE" : "default_theme.thm.json",
	"MY_NAME" : "Lorem"
}
```
Key | Value
----|-------
ICON_FILE | The File used by Tcl/Tk to display the favicon. Do not change this unless you wish to change the favicon.
PYAG_PICS_DIR | This directory contains all `.png` files required for the Autojoiner to function. See below for instructions.
DB_URL | SQLAlchemy DB URI to be used. You can also connect to a common database server and then, Whoa! You have a network-wide Meeting Notice Board!
THEME_FILE | A simple theme file to change the appearance of the window. You can meddle around with the colors, fonts, etc.
MY_NAME | The name Autojoiner will change to when you join the meeting. Required.

### Adding the images to `PYAG_PICS_DIR`

First, pin Zoom to your taskbar. This will be how ZAJ opens Zoom. Then, take screenshots and name the files as below:

All images must be in .png format only.

File Name | Description of the screenshot | Example
----------|-------------------------------|--------
zoom_taskbar.png | A picture of Zoom in the taskbar. | 
join_btn.png | A picture of the blue Join button in the Zoom home screen. to the right of orange New Meeting. | 
name_box.png | A picture of your name in the Join meeting box. Below the Meeting ID prompt. | 
join_btn_after_mtg_id.png | The Join Meeting button in the Enter Passcode page. |
