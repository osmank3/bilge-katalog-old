#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import libilge

EXP = libilge.explore()

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

from PyQt4 import QtCore
from PyQt4 import QtGui
from uiQt_infodialog import Ui_infoDialog

TYPES = {"directory":"dirs", "file":"files"}

class infoDialog(QtGui.QDialog, Ui_infoDialog):
    def __init__(self, type, id):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.type = type
        self.id = id
        
        # signals
        self.connect(self.resetButton, QtCore.SIGNAL("clicked()"), self.parse)
        
        self.parse()
        
    def parse(self):
        if self.type == u"directory":
            self.dirInfos()
            
        elif self.type == "file":
            self.fileInfos()
            
    def dirInfos(self):
        self.detailSW.setCurrentIndex(0)
        self.infoSW.setCurrentIndex(1) # infoSW 0, 1 = fileInfo, DirectoryInfo
        
        self.infos = EXP.info(id=self.id, type=TYPES[str(self.type)], redict=True)
        
        self.dirInfoName.setText(self.infos["name"])
        self.dirInfoDescription.setPlainText(self.infos["description"])
        self.dirInfoDateCreate.setDateTime(self.infos["datecreate"])
        self.dirInfoDateModify.setDateTime(self.infos["datemodify"])
        self.dirInfoDateAccess.setDateTime(self.infos["dateaccess"])
        self.dirInfoDateInsert.setDateTime(self.infos["dateinsert"])
        
    def fileInfos(self):
        pass # doldurulacak burası uygun verilerle
