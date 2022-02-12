;NSIS Modern User Interface
;Welcome/Finish Page Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ; Vars in prog
  !define APPNAME "Zoom Autojoiner GUI"
  !define COMPANYNAME "AMSDC"
  !define DESCRIPTION "To join Zoom Meetings quickly"
  # These three must be integers
  !define VERSIONMAJOR 1
  !define VERSIONMINOR 0
  !define VERSIONBUILD 0
  !define HELPURL "http://advaith.ddns.net:8081/" # "Support Information" link
  !define UPDATEURL "http://advaith.ddns.net:8081/" # "Product Updates" link
  !define ABOUTURL "http://advaith.ddns.net:8081/" # "Publisher" link
  # This is the size (in kB) of all the files copied into "Program Files"
  !define INSTALLSIZE 1034

  !define SOURCEDIR ""
  # EXE file name w/o .exe
  !define LAUNCHEREXE "ZAJ"
  ; use ${LAUNCHEREXE}
  ;Name and file
  Name "${APPNAME}"
  OutFile "${COMPANYNAME}_${APPNAME}_${VERSIONMAJOR}_${VERSIONMINOR}_${VERSIONBUILD}.exe"
  Unicode True

  ;Default installation folder
  InstallDir "$LOCALAPPDATA\${APPNAME}"

  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\${APPNAME}" ""

  ;Request application privileges for Windows Vista
  ;RequestExecutionLevel admin

  ; Tell NSIS to use current user directory
  SetShellVarContext current
  

;--------------------------------
;Interface Settings
  BrandingText "${COMPANYNAME} ${APPNAME} ${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"

  !define MUI_ABORTWARNING
  !define MUI_ICON "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\icon\app.ico"
  !define MUI_UNICON "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\icon\app.ico"

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !define MUI_LICENSEPAGE_RADIOBUTTONS
  !insertmacro MUI_PAGE_LICENSE "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\license\gpl-3.0.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_STARTMENU 0 $SMDir
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

  

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "-Core Files" SecCoreFiles

  SetOutPath "$INSTDIR"

  ;ADD YOUR OWN FILES HERE...
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\${LAUNCHEREXE}.exe"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\lvmem.csv"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\Microsoft.Web.WebView2.Core.dll"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\Microsoft.Web.WebView2.Core.xml"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\Microsoft.Web.WebView2.WinForms.dll"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\Microsoft.Web.WebView2.WinForms.xml"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\Microsoft.Web.WebView2.Wpf.dll"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\Microsoft.Web.WebView2.Wpf.xml"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\WebView2Loader.dll"
  ; file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\icon\app.ico"
  File /oname="$INSTDIR\${LAUNCHEREXE}.exe" "${SOURCEDIR}\${LAUNCHEREXE}.exe"
  ;Store installation folder
  WriteRegStr HKCU "Software\${APPNAME}" "" $INSTDIR

  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${COMPANYNAME} ${APPNAME}"
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$\"$INSTDIR\app.ico$\""
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "HelpLink" "${HELPURL}"
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
	WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
	WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
	WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
	# There is no option for modifying or repairing the install
	WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
	WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
	# Set the INSTALLSIZE constant (!defined at the top of this script) so Add/Remove Programs can accurately report the size
	WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd
;Section "fileappassn32" SecDummy2
;  SetOutPath "$INSTDIR"
;  file "C:\Users\Kannu_Study\Documents\NSIS\fileappassn32.exe"
;  file "C:\Users\Kannu_Study\Documents\NSIS\picview.exe"

;SectionEnd
; Section "Start Menu Shortcut" SecDummy3
;   SetOutPath "$SMPROGRAMS\${COMPANYNAME}"
;   createDirectory "$SMPROGRAMS\${COMPANYNAME}"
;   createShortCut "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk" "$INSTDIR\gmeetwin.exe" "" "$INSTDIR\app.ico"
; SectionEnd

; Section /o "Desktop Shortcut" SecDummy4
;   ;SetOutPath "$DESKTOP"
;   ;createDirectory "$SMPROGRAMS\${COMPANYNAME}"
;   createShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${LAUNCHEREXE}.exe" "" "$INSTDIR\app.ico"
; SectionEnd
Section /o "Updater" SecUpdater
  SetOutPath "$INSTDIR"
  file "C:\Users\Advaith\OneDrive\Documents\Google Meet\Client\v1.0.0\Update.exe"
SectionEnd

; Start Menu

Section -StartMenu
!insertmacro MUI_STARTMENU_WRITE_BEGIN 0 ;This macro sets $SMDir and skips to MUI_STARTMENU_WRITE_END if the "Don't create shortcuts" checkbox is checked... 
CreateDirectory "$SMPrograms\$SMDir"
CreateShortCut "$SMPROGRAMS\$SMDir\${APPNAME}.lnk" "$INSTDIR\${LAUNCHEREXE}.exe" "" "$INSTDIR\app.ico"
!insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecCoreFiles ${LANG_ENGLISH} "Installs ${APPNAME} on your system"
  LangString DESC_SecUpdater ${LANG_ENGLISH} "Installs the Update Daemon on your system to enable faster uptates using the AMSDC API."
  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecCoreFiles} $(DESC_SecCoreFiles)
    ;!insertmacro MUI_DESCRIPTION_TEXT ${SecDummy2} $(DESC_SecDummy2)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecUpdater} $(DESC_SecUpdater)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...
  ;!insertmacro MUI_STARTMENU_GETFOLDER Application "GlobalSpectrum"

  Delete "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk"
  RMDir "$SMPROGRAMS\${COMPANYNAME}"
  
  Delete "$DESKTOP\${APPNAME}.lnk"

  ;uninst
  RMDir /r "$INSTDIR\gmeetwin.exe.WebView2"
  Delete "$INSTDIR\${LAUNCHEREXE}.exe"
  Delete "$INSTDIR\Update.exe"
  Delete "$INSTDIR\lvmem.csv"
  Delete "$INSTDIR\Microsoft.Web.WebView2.Core.dll"
  Delete "$INSTDIR\Microsoft.Web.WebView2.Core.xml"
  Delete "$INSTDIR\Microsoft.Web.WebView2.WinForms.dll"
  Delete "$INSTDIR\Microsoft.Web.WebView2.WinForms.xml"
  Delete "$INSTDIR\Microsoft.Web.WebView2.Wpf.dll"
  Delete "$INSTDIR\Microsoft.Web.WebView2.Wpf.xml"
  Delete "$INSTDIR\WebView2Loader.dll"
  Delete "$INSTDIR\app.ico"
  
  ;keep last
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\${APPNAME}"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"


SectionEnd
