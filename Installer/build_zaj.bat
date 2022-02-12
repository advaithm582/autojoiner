cd ..
CALL venv\Scripts\activate
cd Installer
py get_files.py vi
pyinstaller ZoomAutojoinerGUI.py --onedir -i=ZoomAJIcon.ico --version-file=zaj_verinfo.txt --noconsole --noconfirm
xcopy ZoomAJIcon.ico dist\ZoomAutojoinerGUI
py get_files.py nsis
pause