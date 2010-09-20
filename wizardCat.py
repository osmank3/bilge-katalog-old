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
from uiQt_createcatalogwizard import Ui_createCatalogWizard

class CreateCat(QtGui.QWizard, Ui_createCatalogWizard):
    def __init__(self):
        QtGui.QWizard.__init__(self)
        self.setupUi(self)
        
        self.setOption(QtGui.QWizard.DisabledBackButtonOnLastPage)
        self.setOption(QtGui.QWizard.NoBackButtonOnStartPage)
        
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
            elif self.lineDirPath.text() == u"" and self.fillRadio.isChecked():
                back = True
            else:
                self.fillConf()
            if back:
                self.back()
        elif pageId == 3:
            self.finish()
                
    def chooseDir(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(options = QtGui.QFileDialog.ShowDirsOnly)
        self.lineDirPath.setText(dirname)
        
    def fillConf(self):
        Text = ""
        Text += "%15s : %s\n"%("Name", str(self.lineName.text()))
        Text += "%15s : %s\n"%("Description", str(self.lineDesc.toPlainText()))
        Text += "%15s : %s\n"%("Date", self.dateTimeEdit.dateTime().toString())
        directory = self.lineDirPath.text()
        if directory != u"":
            Text += "%15s : %s\n"%("Directory", directory)
        self.lineConf.insertPlainText(Text)
        
    def finish(self):
        self.setEnabled(False)
        self.catalog2DB()
        self.setEnabled(True)
        
    def catalog2DB(self):
        info = {}
        info["name"] = str(self.lineName.text())
        info["description"] = str(self.lineDesc.toPlainText())
        info["dateinsert"] = self.dateTimeEdit.dateTime().toPyDateTime()
        info["up_id"] = 0
        directory = self.lineDirPath.text()
        if directory == u"":
            directory = None
        else:
            directory = str(directory)
        EXP.mkDir(address=directory, infos=info)
            
