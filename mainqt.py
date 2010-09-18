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
        
        #signals
        self.connect(self.listCat, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.fillFilesList)
        self.connect(self.listFiles, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.fillFilesList)
        #signals of actions
        self.actExit.triggered.connect(self.Exit)
        
    def fillCatList(self):
        dirs, files = EXP.dirList(id=0, partite=True)
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
            
    def Exit(self):
        sys.exit()
        
    def fillFilesList(self, itemSelected):
        type, id = str(itemSelected.whatsThis()).split()
        if type == "directory":
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
                
      
app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
