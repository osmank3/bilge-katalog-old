#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

if "create" in sys.argv:
    liste = os.listdir("qt/ui")
    for i in liste:
        if i[-2:] == "ui":
            os.system("pyuic4 qt/ui/%s -o qt/uiQt_%s.py"% (i, i[:-3]))
        elif i[-3:] == "qrc":
            os.system("pyrcc4 qt/ui/%s -o qt/%s_rc.py"% (i, i[:-4]))
        
elif "delete" in sys.argv:
    liste = os.listdir("qt")
    for i in liste:
        if i.find("uiQt_") != -1 or i.find("_rc.py") != -1:
            os.remove("qt/" + i)
