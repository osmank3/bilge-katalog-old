#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import bilge_katalog.inserting as inserting

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

from PyQt4 import QtCore
from PyQt4 import QtGui
from uiQt_createcatalogwizard import Ui_createCatalogWizard

class CreateCat(QtGui.QWizard, Ui_createCatalogWizard):
    def __init__(self):
        QtGui.QWizard.__init__(self)
        self.setupUi(self)
        
        self.labelStat.setHidden(True)
        self.progressBar.setValue(0)
        
        #signals
        self.connect(self.buttonChoseDir, QtCore.SIGNAL("clicked()"), self.chooseDir)
        self.connect(self, QtCore.SIGNAL("currentIdChanged(int)"), self.nextPage)
        
    def nextPage(self, pageId):
        if pageId == 0:
            self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        elif pageId == 1:
            back = False
            if self.lineName.text() == u"":
                back = True
            elif self.lineDirPath.text() == u"" and self.lineDirPath.isEnabled():
                back = True
            if back:
                self.back()
            else:
                self.startCataloging()
                
    def chooseDir(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(options = QtGui.QFileDialog.ShowDirsOnly)
        self.lineDirPath.setText(dirname)
        
    def startCataloging(self):
        self.catalog = inserting.Item("directory", {"up_id":0,
                                               "name":str(self.lineName.text()),
                                               "description":str(self.lineDesc.toPlainText()),
                                               "dateinsert":self.dateTimeEdit.dateTime().toPyDateTime()})
        
        if self.lineDirPath.isEnabled():
            self.catalog.setAddress(str(self.lineDirPath.text()))
            self.progressItem = progress(str(self.lineDirPath.text()))
        else:
            self.progressItem = progress()
        
        self.connect(self.progressItem, QtCore.SIGNAL("progressStat(int)"), self.progressBar.setValue)
        self.connect(self.progressItem, QtCore.SIGNAL("finished(bool)"), self.labelStat, QtCore.SLOT("setVisible(bool)"))
        self.connect(self.progressItem, QtCore.SIGNAL("refresh"), self.repaint)
            
        self.setCursor(QtCore.Qt.WaitCursor)
        
        inserting.createDir(self.catalog, self.progressItem)
        
        self.setCursor(QtCore.Qt.ArrowCursor)
        
class progress(QtCore.QObject):
        """İlerleme yüzdesini göstermek için yazılan nesne."""
        numOfItems = 0
        curNum = 0
        
        def __init__(self, address=None):
            """İlerleme yüzdesi oluşturma sınıfı
            
            progress(address=None)"""
            QtCore.QObject.__init__(self)
            if address:
                self.numOfItems = self.getNumOfItems(address) + 1
            else:
                self.numOfItems = 1
                
        def getNumOfItems(self, address):
            """Verilen adresteki dosya ve dizinlerin sayısını dönen fonksiyon.
            
            getNumOfItems(address)"""
            oldDir = os.getcwd()
            os.chdir(address)
            dirList = os.listdir("./")
            numOfItems = len(dirList)
            
            for i in dirList:
                if os.path.isdir(i):
                    numOfItems += self.getNumOfItems(i)
                    
            os.chdir(oldDir)
            return numOfItems
            
        def increase(self):
            """İşlenenlerin sayısını bir artıran fonksiyon."""
            self.curNum += 1
            self.showPercent()
            
        def getPercent(self):
            """İşlenenlerin yüzdesini dönen fonksiyon."""
            percent = 100 * self.curNum / self.numOfItems
            return percent
            
        def showPercent(self):
            if self.getPercent() == 100:
                self.emit(QtCore.SIGNAL("progressStat(int)"), self.getPercent())
                self.emit(QtCore.SIGNAL("finished(bool)"), True)
            else:
                self.emit(QtCore.SIGNAL("progressStat(int)"), self.getPercent())
                self.emit(QtCore.SIGNAL("refresh"))
