#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import libilge

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

from PyQt4 import QtCore
from PyQt4 import QtGui
from uiQt_createcatalogwizard import Ui_createCatalogWizard

class CreateCat(QtGui.QWizard, Ui_createCatalogWizard):
    def __init__(self):
        QtGui.QWizard.__init__(self)
        self.setupUi(self)
        
        #signals
        self.connect(self.buttonChoseDir, QtCore.SIGNAL("clicked()"), self.chooseDir)
        self.connect(self, QtCore.SIGNAL("currentIdChanged(int)"), self.nextPage)
        
    def nextPage(self, pageId):
        if pageId == 1:
            self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        elif pageId == 2:
            back = False
            if self.lineName.text() == u"":
                back = True
            if self.lineDirPath.text() == u"" and self.fillRadio.isChecked():
                back = True
            if back:
                self.back()
                
        elif pageId == 3:
            self.catalog2DB()
                
    def chooseDir(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(options = QtGui.QFileDialog.ShowDirsOnly)
        self.lineDirPath.setText(dirname)
        
    def catalog2DB(self):
        info = {}
        info["name"] = str(self.lineName.text())
        info["description"] = str(self.lineDesc.toPlainText())
        info["dateinsert"] = self.dateTimeEdit.dateTime().toPyDateTime()
        info["up_id"] = 0
        directory = self.lineDirPath.text()
        if directory != u"":
            print info, directory # ilgili fonksiyona yönlendirme yapılacak
        else:
            print info # ilgili fonksiyona yönlendirme yapılacak
            
