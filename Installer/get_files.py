import glob
import os
import sys
import csv

import chevron

if len(sys.argv) > 1:
    # vma = int(input("Enter major version: "))
    # vmi = int(input("Enter minor version: "))
    # vbd = int(input("Enter build version: "))
    vma, vmi, vbd = 0, 4, 2
    if sys.argv[1]=="nsis":
        print("nsis generation")
        os.chdir("dist/ZoomAutojoinerGUI")

        files = []
        dirs = []
        # for fil in glob.glob("*"):
        #     files.append({"file_name":fil})
            
        for fil in glob.glob("**/*", recursive=True):
            if os.path.isfile(fil):
                files.append({"file_name":fil})
            elif os.path.isdir(fil):
                dirs.append({"dir_name":fil})
        # for fil in glob.glob("**/*", recursive=True):
        #     dirs.append({"dir_name":fil})
            
            
        spdirs = [{"dir_name": d}
                for d in ["config", "extensions", "logs", "themes"]]
        
        spdel = [{"file_name": d}
                for d in ["database.db","config_tool.exe"]]
                
        csvfh =  open("../../_extensions/extensions.csv", "r")
        extensions = csv.DictReader(csvfh, fieldnames=('codename','name','desc'))
        # for i in dr:
            # print(i['codename'], i['name'], i['desc'])
        
        variables = {
            "source_directory": os.getcwd(),
            "versionmajor": vma,
            "versionminor": vmi,
            "versionbuild": vbd,
            "url": "https://advaithm582.github.io/",
            "files": files,
            "dirs": dirs,
            "spdirs": spdirs,
            "spdel": spdel,
            "extensions": list(extensions),
            "icon_file": "ZoomAJIcon.ico",
            "launcher_exe": "ZoomAutojoinerGUI",
            "license_file": r"C:\Users\advai\OneDrive\Documents\Programmed tools\Autojoiner\Installer\LICENSE.txt"
        }

        of = open("../../InstallerScript.nsi", "w")

        with open('../../InstallerScript.nsi.mustache', 'r') as f:
            of.write(chevron.render(f, variables))

        of.close()
        csvfh.close()
    elif sys.argv[1]=="vi":
        print("Version info generation")
        variables = {
            "versionmajor": vma,
            "versionminor": vmi,
            "versionbuild": vbd
        }

        of = open("zaj_verinfo.txt", "w")

        with open('zaj_verinfo.txt.mustache', 'r') as f:
            of.write(chevron.render(f, variables))
            
        of.close()
else:
    print("Error", sys.argv)
