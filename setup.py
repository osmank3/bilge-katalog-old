#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import shutil
import platform
import constants
from distutils.core import setup

argv = sys.argv

if os.name == "posix" and platform.system() == "Linux":
    def createQtFiles():
        listOfFiles = os.listdir("uiQt")
        for i in listOfFiles:
            if i[-2:] == "ui":
                print "%s is compiling..."% i
                os.system("pyuic4 uiQt/%s -o uiQt_%s.py"% (i, i[:-3]))
            elif i[-3:] == "qrc":
                print "%s is compiling..."% i
                os.system("pyrcc4 uiQt/%s -o %s_rc.py"% (i, i[:-4]))
    
    def createPackege():
        os.mkdir("bilge_katalog")
        listOfFiles = glob.glob("*.py")
        listOfFiles.remove("setup.py")
        for i in listOfFiles:
            shutil.copy(i, "bilge_katalog/")
        init = open("bilge_katalog/__init__.py", "w")
        init.write("#!/usr/bin/python")
        init.close()
        
    def createLocale():
        localeDir = "locale/"
        os.mkdir(localeDir)
        datalist = []
        po_list = glob.glob("po/*.po")
        for i in po_list:
            po = os.path.split(i)[-1]
            lang = po[:-3]
            mo = localeDir + lang + "/bilge-katalog.mo"
            
            print "%s is compiling..."% po
            os.mkdir(localeDir + lang + "/")
            os.system("msgfmt %s -o %s"% (i, mo))
            
        ts_list = glob.glob("uiQt/locale/*.ts")
        ts_list.remove("uiQt/locale/bilge-katalog.ts")
        for i in ts_list:
            ts = os.path.split(i)[-1]
            lang = ts[:-3]
            qm = localeDir + lang + "/bilge-katalog.qm"
            
            print "%s is compiling..."% ts
            try:
                os.mkdir(localeDir + lang + "/")
            except:
                pass
            os.system("lrelease %s -qm %s"% (i, qm))
            
        return buildedLocaleData()
        
    def buildedLocaleData():
        datalist = []
        listOfFiles = glob.glob("locale/*/*")
        for i in listOfFiles:
            lang= i.split("/")[-2]
            datalist.append(("share/locale/%s/LC_MESSAGES"% lang, [i]))
            
        return datalist
        
    def removeBuild():
        dirsToRemove = ["bilge_katalog", "locale", "build"]
        filesToRemove = glob.glob("ui*.py")
        filesToRemove += glob.glob("*_rc.py")
        
        for i in dirsToRemove:
            try:
                shutil.rmtree(i)
                print "%s is removed"% i
            except:
                pass
            
        for i in filesToRemove:
            try:
                os.remove(i)
                print "%s is removed"% i
            except:
                pass
    
    def isBuilded():
        listOfFiles = set(os.listdir("./"))
        if set(["bilge_katalog", "locale", "build"]).issubset(listOfFiles):
            return True
        else:
            removeBuild() # this is for cleaning
            return False
    
    if "remove" in argv:
        removeBuild()
    else:
        if not isBuilded():
            createQtFiles()
            createPackege()
            datalist = createLocale()
            
        else:
            datalist = buildedLocaleData()
            
        data = [("share/applications", ["data/Bilge-Katalog-Qt4.desktop"]),
                ("share/pixmaps", ["images/bilge-katalog.png"])]
            
        data.extend(datalist)
        
        setup(
            name = constants.NAME,
            version = constants.VERSION,
            description = constants.DESCRIPTION,
            author = constants.CORE_DEVELOPER,
            author_email = constants.CORE_EMAIL,
            url = constants.URL,
            license = constants.LICENSE_NAME,
            packages = ["bilge_katalog"],
            scripts = ["bilge-katalog"],
            data_files = data,
            )