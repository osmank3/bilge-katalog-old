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
        self.exploreToolBar.addAction(self.actBack)
        self.exploreToolBar.addAction(self.actNext)
        self.exploreToolBar.addAction(self.actUp)
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
        
        # Files list context menu
        self.actInfoFile = QtGui.QAction(self)
        self.actInfoFile.setText(QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        
        self.viewFiles.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.viewFiles.addAction(self.menuNew.menuAction())
        self.viewFiles.addAction(self.actDel)
        self.viewFiles.addAction(self.actCut)
        self.viewFiles.addAction(self.actCopy)
        self.viewFiles.addAction(self.actPaste)
        self.viewFiles.addAction(self.actInfoFile)
        
        # Catalogs list context menu
        
        self.actInfoCat = QtGui.QAction(self)
        self.actInfoCat.setText(QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        
        self.viewCat.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.viewCat.addAction(self.actCreateCatalog)
        self.viewCat.addAction(self.actDel)
        self.viewCat.addAction(self.actPaste)
        self.viewCat.addAction(self.actInfoCat)
        
        # signals
        self.connect(self.listCat, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.doubleClickAction)
        self.connect(self.listFiles, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.doubleClickAction)
        # signals of actions
        self.actBack.triggered.connect(self.Back)
        self.actNext.triggered.connect(self.Next)
        self.actUp.triggered.connect(self.Up)
        self.actCreateCatalog.triggered.connect(self.createCat)
        self.actInfoFile.triggered.connect(self.infoFileAction)
        self.actInfoCat.triggered.connect(self.infoCatAction)
        self.actNewFile.triggered.connect(self.newFile)
        self.actNewDir.triggered.connect(self.newDir)
        
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
            if self.history[-1] != id:
                self.history.append(id)
                self.indexNow += 1
        if type == "file":
            self.openInfo(type=type, id=id)
            
    def infoFileAction(self):
        item = self.listFiles.currentItem()
        type, id = str(item.whatsThis()).split()
        self.openInfo(type=str(type), id=id)
        
    def infoCatAction(self):
        item = self.listCat.currentItem()
        type, id = str(item.whatsThis()).split()
        self.openInfo(type=str(type), id=id, cat=True)
        
    def newFile(self):
        type = "file"
        self.openInfo(type=str(type), id=-1)
        
    def newDir(self):
        type = "directory"
        self.openInfo(type=str(type), id=-1)
            
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
        
    def openInfo(self, type, id, cat=False):
        dirId = self.history[self.indexNow]
        if cat:
            itemInfos = infoDialog.infoDialog(type=type, id=id, upid=0)
        else:
            itemInfos = infoDialog.infoDialog(type=type, id=id, upid=dirId)
        itemInfos.exec_()
        self.fillCatList()
        if dirId != 0:
            self.fillFilesList(id=dirId)
                
      
app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
