#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import libilge

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

from PyQt4 import QtCore
from PyQt4 import QtGui
from uiQt_mainwindow import Ui_MainWindow

import wizardCat
import infoDialog

EXP = libilge.explore()

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.splitter.setStretchFactor(1,1)
        # list view for catalogs -> 0, 1 = list, tree
        self.viewCat.setCurrentIndex(0)
        # list view for files and folders -> 0, 1, 2 = list, table, icon
        self.viewFiles.setCurrentIndex(0)
        self.fillCatList()
        
        self.history = [0]
        self.indexNow = 0
        
        # toolbars
        self.addressToolBar.addAction(self.actBack)
        self.addressToolBar.addAction(self.actNext)
        self.addressToolBar.addAction(self.actUp)
        self.editToolBar.addAction(self.actCut)
        self.editToolBar.addAction(self.actCopy)
        self.editToolBar.addAction(self.actPaste)
        self.editToolBar.addAction(self.actDel)
        
        self.searchLine = QtGui.QLineEdit()
        self.searchButton = QtGui.QPushButton()
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Search")
        self.searchToolBar.addWidget(self.searchLine)
        self.searchToolBar.addWidget(self.searchButton)
        
        # context menu
        self.actInfo = QtGui.QAction(self)
        self.actInfo.setText(QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.addAction(self.actCut)
        self.addAction(self.actCopy)
        self.addAction(self.actPaste)
        self.addAction(self.actDel)
        self.addAction(self.actInfo)
        
        # signals
        self.connect(self.listCat, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.doubleClickAction)
        self.connect(self.listFiles, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.doubleClickAction)
        # signals of actions
        self.actBack.triggered.connect(self.Back)
        self.actNext.triggered.connect(self.Next)
        self.actUp.triggered.connect(self.Up)
        self.actCreateCatalog.triggered.connect(self.createCat)
        self.actInfo.triggered.connect(self.infoAction)
        
    def fillCatList(self):
        dirs, files = EXP.dirList(id=0, partite=True)
        self.listCat.clear()
        for i in dirs.keys():
            item = QtGui.QListWidgetItem()
            item.setText(i)
            item.setWhatsThis("directory %s"% dirs[i])
            self.listCat.addItem(item)
        for i in files.keys():
            item = QtGui.QListWidgetItem()
            item.setText(i)
            item.setWhatsThis("file %s"% files[i])
            self.listCat.addItem(item)
    
    def fillFilesList(self, id):
        dirs, files = EXP.dirList(id=id, partite=True)
        self.listFiles.clear()
        for i in dirs.keys():
            item = QtGui.QListWidgetItem()
            item.setText(i)
            item.setWhatsThis("directory %s"% dirs[i])
            self.listFiles.addItem(item)
        for i in files.keys():
            item = QtGui.QListWidgetItem()
            item.setText(i)
            item.setWhatsThis("file %s"% files[i])
            self.listFiles.addItem(item)
        
    def doubleClickAction(self, itemSelected):
        type, id = str(itemSelected.whatsThis()).split()
        if type == "directory":
            self.fillFilesList(id=id)
            self.history = self.history[:self.indexNow+1]
            self.history.append(id)
            self.indexNow += 1
        if type == "file":
            self.openInfo(type=type, id=id)
            
    def infoAction(self):
        item = self.listFiles.currentItem()
        type, id = str(item.whatsThis()).split()
        self.openInfo(type=str(type), id=id)
            
    def Back(self):
        if self.indexNow != 0:
            id = self.history[self.indexNow - 1]
            self.fillFilesList(id=id)
            self.indexNow -= 1
        
    def Next(self):
        if self.indexNow + 1 < len(self.history):
            id = self.history[self.indexNow + 1]
            self.fillFilesList(id=id)
            self.indexNow += 1
        
    def Up(self):
        if self.indexNow != 0 and self.history[self.indexNow] != 0:
            EXP.chDir(id=self.history[self.indexNow])
            EXP.chDir(dirname="..")
            id = EXP.dirNow
            self.fillFilesList(id=id)
            self.history = self.history[:self.indexNow+1]
            self.history.append(id)
            self.indexNow += 1
            
    def createCat(self):
        crCat = wizardCat.CreateCat()
        crCat.exec_()
        self.fillCatList()
        
    def openInfo(self, type, id):
        dirId = self.history[self.indexNow]
        itemInfos = infoDialog.infoDialog(type=type, id=id)
        itemInfos.exec_()
        self.fillCatList()
        self.fillFilesList(id=dirId)
                
      
app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
