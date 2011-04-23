#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import bridge_qt

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

from PyQt4 import QtCore
from PyQt4 import QtGui
from uiQt_mainwindow import Ui_MainWindow

import wizardCat
#import infoDialog
#import aboutDialog
#import userDialog
#import lendDialog

EXP = bridge_qt.ExploreQt()

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
        
        self.history = []
        self.indexNow = -1
        self.searching = False
        self.willPaste = None
        self.pasteType = None
        
        # toolbars
        self.exploreToolBar.addAction(self.actBack)
        self.exploreToolBar.addAction(self.actNext)
        self.exploreToolBar.addAction(self.actUp)
        self.exploreToolBar.addAction(self.actRefresh)
        self.editToolBar.addAction(self.actCut)
        self.editToolBar.addAction(self.actCopy)
        self.editToolBar.addAction(self.actPaste)
        self.editToolBar.addAction(self.actDel)
        
        self.searchLine = QtGui.QLineEdit()
        self.searchButton = QtGui.QPushButton()
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/images/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchButton.setIcon(icon)
        self.searchToolBar.addWidget(self.searchLine)
        self.searchToolBar.addWidget(self.searchButton)
        
        # Files context menu
        self.contextFilesMenu = QtGui.QMenu(self.viewFiles)
        self.contextFilesMenu.addAction(self.menuNew.menuAction())
        self.contextFilesMenu.addAction(self.actDel)
        self.contextFilesMenu.addAction(self.actCut)
        self.contextFilesMenu.addAction(self.actCopy)
        self.contextFilesMenu.addAction(self.actPaste)
        self.contextFilesMenu.addAction(self.actLending)
        self.contextFilesMenu.addAction(self.actInfo)
        
        # Catalogs context menu
        self.contextCatsMenu = QtGui.QMenu(self.viewCat)
        self.contextCatsMenu.addAction(self.actCreateCatalog)
        self.contextCatsMenu.addAction(self.actDel)
        self.contextCatsMenu.addAction(self.actPaste)
        self.contextCatsMenu.addAction(self.actLending)
        self.contextCatsMenu.addAction(self.actInfo)
        
        # signals
        self.connect(self.listCat, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.doubleClickAction)
        self.connect(self.listFiles, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.doubleClickAction)
        self.connect(self.listCat, QtCore.SIGNAL("itemClicked(QListWidgetItem *)"), self.clickAction)
        self.connect(self.listFiles, QtCore.SIGNAL("itemClicked(QListWidgetItem *)"), self.clickAction)
        self.connect(self.viewFiles, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.contextFiles)
        self.connect(self.viewCat, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.contextCats)
        self.connect(self.searchButton, QtCore.SIGNAL("clicked()"), self.search)
        self.connect(self.searchLine, QtCore.SIGNAL("returnPressed()"), self.searchButton, QtCore.SLOT("click()"))
        self.connect(self.searchLine, QtCore.SIGNAL("textChanged(QString)"), self.searchButtonStatus)
        # signals of actions
        self.actBack.triggered.connect(self.Back)
        self.actNext.triggered.connect(self.Next)
        self.actUp.triggered.connect(self.Up)
        self.actCreateCatalog.triggered.connect(self.createCat)
        self.actInfo.triggered.connect(self.infoAction)
        self.actNewFile.triggered.connect(self.newFile)
        self.actNewDir.triggered.connect(self.newDir)
        self.actDel.triggered.connect(self.delete)
        self.actCopy.triggered.connect(self.copy)
        self.actCut.triggered.connect(self.cut)
        self.actPaste.triggered.connect(self.paste)
        self.actRefresh.triggered.connect(self.refresh)
        self.actAbout.triggered.connect(self.about)
        self.actLending.triggered.connect(self.lend)
        self.actUserInfo.triggered.connect(self.users)
        self.actNewUser.triggered.connect(self.newUser)

    def contextFiles(self, point):
        self.item = None
        self.item = self.listFiles.itemAt(point)
        if not self.item:
            if self.history[self.indexNow] != 0:
                infos = EXP.info(id=self.history[self.indexNow],
                                 type="dirs", redict=True)
            else:
                infos = {"name":"/"}
            self.item = QtGui.QListWidgetItem()
            self.item.setText(infos["name"])
            self.item.setWhatsThis("directory %s"% self.history[self.indexNow])
            
        coordinate = self.viewFiles.mapToGlobal(point)
        self.contextFilesMenu.exec_(coordinate)
        
    def contextCats(self, point):
        self.item = None
        self.item = self.listCat.itemAt(point)
        if not self.item:
            infos = {"name":"/"}
            self.item = QtGui.QListWidgetItem()
            self.item.setText(infos["name"])
            self.item.setWhatsThis("directory %s"% self.history[self.indexNow])
        
        coordinate = self.viewCat.mapToGlobal(point)
        self.contextCatsMenu.exec_(coordinate)
        
    def fillCatList(self):
        self.listCat.clear()
        for i in EXP.fillListQt(bridge_qt.RootItemQt()):
            if i.form == "directory":
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/image/images/bilge-katalog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                i.setIcon(icon)
                i.setText(i.name)
                self.listCat.addItem(i)
    
    def fillFilesList(self, item):
        EXP.chdir(item)
        self.listFiles.clear()
        for i in EXP.curItemList:
            if i.form == "directory":
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/image/images/directory.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                i.setIcon(icon)
                i.setText(i.name)
                self.listFiles.addItem(i)
            elif i.form == "file":
                i.setDetail()
                icon = QtGui.QIcon()
                
                if i.info["type"] == "book":
                    icon.addPixmap(QtGui.QPixmap(":/image/images/book.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                elif i.info["type"] == "ebook":
                    icon.addPixmap(QtGui.QPixmap(":/image/images/ebook.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                elif i.info["type"] == "image":
                    icon.addPixmap(QtGui.QPixmap(":/image/images/image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                elif i.info["type"] == "music":
                    icon.addPixmap(QtGui.QPixmap(":/image/images/music.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                elif i.info["type"] == "video":
                    icon.addPixmap(QtGui.QPixmap(":/image/images/video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                else:
                    icon.addPixmap(QtGui.QPixmap(":/image/images/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                i.setIcon(icon)
                i.setText(i.name)
                self.listFiles.addItem(i)
        
    def refresh(self):
        self.fillCatList()
        if not self.indexNow in [-1,0] and not self.searching:
            self.fillFilesList(self.history[self.indexNow])
            self.searchLine.clear()
        
    def doubleClickAction(self, itemSelected):
        if itemSelected.form == "directory":
            self.fillFilesList(itemSelected)
            self.history = self.history[:self.indexNow+1]
            if len(self.history) == 0 or self.history[-1].no != itemSelected.no:
                self.history.append(itemSelected)
                self.indexNow += 1
            if self.searching:
                self.searching = False
                self.searchLine.clear()
        elif itemSelected.form == "file":
            pass#self.openInfo(type=type, id=id) #dosya bilgilerini gösteren pencere açılacak
            
    def clickAction(self, itemSelected):
        self.item = itemSelected
            
    def infoAction(self):
        if self.item.text() != "/":
            type, id = str(self.item.whatsThis()).split()
            self.openInfo(type=str(type), id=id)
        
    def newFile(self):
        upid = str(self.item.whatsThis()).split()[-1]
        type = "file"
        self.openInfo(type=str(type), id=None, upid=upid)
        
    def newDir(self):
        upid = str(self.item.whatsThis()).split()[-1]
        type = "directory"
        self.openInfo(type=str(type), id=None, upid=upid)
            
    def Back(self):
        if self.searching:
            self.searching = False
            self.searchLine.clear()
            self.refresh()
        elif not self.indexNow in [-1,0]:
            item = self.history[self.indexNow - 1]
            self.fillFilesList(item)
            self.indexNow -= 1
        
    def Next(self):
        if self.searching:
            self.searching = False
            self.searchLine.clear()
            self.refresh()
        elif self.indexNow + 1 < len(self.history):
            item = self.history[self.indexNow + 1]
            self.fillFilesList(item)
            self.indexNow += 1
        
    def Up(self):
        if self.searching:
            self.searching = False
            self.searchLine.clear()
            self.refresh()
        elif self.indexNow != 0:
            if len(self.history) == 0 or self.history[self.indexNow].updir == None:
                pass
            elif self.history[self.indexNow].updir.no == self.history[self.indexNow-1].no:
                self.Back()
            elif self.history[self.indexNow].updir.no != 0:
                EXP.curItem = self.history[self.indexNow].updir
                self.history = self.history[:self.indexNow+1]
                self.history.append(EXP.curItem)
                self.indexNow += 1
                self.refresh()
            
    def createCat(self):
        crCat = wizardCat.CreateCat()
        crCat.exec_()
        self.refresh()
        
    def openInfo(self, type, id, upid=None):
        itemInfos = infoDialog.infoDialog(type=type, id=id, upid=upid)
        itemInfos.exec_()
        self.refresh()
            
    def delete(self):
        type, id = str(self.item.whatsThis()).split()
        self.setCursor(QtCore.Qt.WaitCursor)
        if type == "file":
            EXP.delFile(id=id)
        elif type == "directory":
            EXP.delDir(id=id)
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.refresh()
        
    def copy(self):
        self.willPaste = (str(self.item.text()), self.history[self.indexNow])
        self.pasteType = "copy"
        
    def cut(self):
        self.willPaste = (str(self.item.text()), self.history[self.indexNow])
        self.pasteType = "cut"
        
    def paste(self):
        newUpType, newUpId = str(self.item.whatsThis()).split()
        if self.willPaste and newUpType == "directory":
            self.setCursor(QtCore.Qt.WaitCursor)
            name, oldUpId = self.willPaste
            if self.pasteType == "cut":
                infos = {"up_id":newUpId}
                
                dirnow = EXP.dirNow
                EXP.chDir(id=oldUpId)
                EXP.update(updated=name, parameters=infos)
                EXP.dirNow = dirnow
                
                self.willPaste = None
            elif self.pasteType == "copy":
                to = EXP.parseAddress(EXP.genAddress(newUpId))
                
                dirnow = EXP.dirNow
                EXP.chDir(id=oldUpId)
                EXP.copy(name=name, to=to)
                EXP.dirNow = dirnow
                
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.refresh()
                
        elif newUpType == "file":
            # ekrana hata mesajı bastırmalı
            print _("This selection is not a directory.")
            
    def searchButtonStatus(self, string):
        if string == "":
            self.searchButton.setEnabled(False)
        else:
            self.searchButton.setEnabled(True)
            
    def search(self):
        self.searching = True
        wanted = str(self.searchLine.text())
        listOfFounded = EXP.search(wanted, "basic") # [(id, name, address, dir or file)]
        self.listFiles.clear()
        self.setCursor(QtCore.Qt.WaitCursor)
        for i in listOfFounded:
            item = QtGui.QListWidgetItem()
            item.setText(i[1])
            if i[3] == "dirs":
                item.setWhatsThis("directory %s"% i[0])
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/image/images/directory.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            elif i[3] == "files":
                item.setWhatsThis("file %s"% i[0])
                icon = self.setFileIcon(i[0])
            item.setIcon(icon)
            self.listFiles.addItem(item)
        self.setCursor(QtCore.Qt.ArrowCursor)
    
    def about(self):
        about = aboutDialog.aboutDialog()
        about.exec_()

    def lend(self):
        type, id = str(self.item.whatsThis()).split()
        lending = lendDialog.lendDialog(type, id)
        lending.exec_()
        
    def users(self):
        users = userDialog.userDialog()
        users.exec_()
        
    def newUser(self):
        users = userDialog.userDialog(new=True)
        users.exec_()
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    #language = QtCore.QLocale.system().name()
    #locale = "/usr/share/locale/%s/LC_MESSAGES"% language
    #if not os.path.isdir(locale):
    #    locale = "/usr/share/locale/%s/LC_MESSAGES"% language[:2]
    #translator = QtCore.QTranslator()
    #translator.load("bilge-katalog.qm", locale)
    #app.installTranslator(translator)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
