#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import libilge
import database
import datetime

from detailer import getKeys

Query = database.EditQuery()
EXP = libilge.explore()

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

from PyQt4 import QtCore
from PyQt4 import QtGui
from uiQt_infodialog import Ui_infoDialog

TYPES = {"directory":"dirs", "file":"files"}

class infoDialog(QtGui.QDialog, Ui_infoDialog):
    def __init__(self, type, id, upid=None):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.type = type
        self.id = id
        if self.id == None:
            self.new = True
            self.upid = upid
        else:
            self.new = False
            
            Query.setStatTrue("select")
            Query.setSelect(["up_id"])
            Query.setTables(["dirs"])
            Query.setWhere({"id":self.id})
            self.upid = database.dataBase().execute(Query.returnQuery())[0][0]
        
        # signals
        self.connect(self.resetButton, QtCore.SIGNAL("clicked()"), self.parse)
        self.connect(self.applyButton, QtCore.SIGNAL("clicked()"), self.applyAction)
        self.connect(self.fillFromFile, QtCore.SIGNAL("clicked()"), self.fillFileInfo)
        self.connect(self.fillFromDir, QtCore.SIGNAL("clicked()"), self.fillDirInfo)
        
        self.parse()
        
    def parse(self):
        if self.type == "directory":
            self.fillFromDir.setEnabled(self.new)
            if self.new:
                self.setNewDirDialog()
            else:
                self.dirInfos()
            
        elif self.type == "file":
            self.fillFromFile.setEnabled(self.new)
            if self.new:
                self.setNewFileDialog()
            else:
                self.fileInfos()
            
    def dirInfos(self):
        self.infoTypeCombo.setCurrentIndex(5) #self.detailSW.setCurrentIndex(5)
        self.infoSW.setCurrentIndex(1) # infoSW 0, 1 = fileInfo, DirectoryInfo
        
        self.infos = EXP.info(id=self.id, type=TYPES[str(self.type)], redict=True)
        
        self.dirInfoName.setText(self.infos["name"])
        self.dirInfoAddress.setText(self.infos["address"])
        self.dirInfoDescription.setPlainText(self.infos["description"])
        self.dirInfoDateCreate.setDateTime(self.infos["datecreate"])
        self.dirInfoDateModify.setDateTime(self.infos["datemodify"])
        self.dirInfoDateAccess.setDateTime(self.infos["dateaccess"])
        self.dirInfoDateInsert.setDateTime(self.infos["dateinsert"])
        
    def fileInfos(self):
        self.infoSW.setCurrentIndex(0)
        
        self.infos = EXP.info(id=self.id, type=TYPES[str(self.type)], redict=True)
        
        if self.infos["size"] < 1024:
            self.infos["sizemode"] = " b"
        elif self.infos["size"] < 1024**2:
            self.infos["sizemode"] = " Kb"
            self.infos["size"] = float(self.infos["size"])/1024
        elif self.infos["size"] < 1024**3:
            self.infos["sizemode"] = " Mb"
            self.infos["size"] = float(self.infos["size"])/(1024**2)
        elif self.infos["size"] >= 1024**3:
            self.infos["sizemode"] = " Gb"
            self.infos["size"] = float(self.infos["size"])/(1024**3)
        
        self.infoSizeSpin.setValue(self.infos["size"])
        self.infos["size"] = self.infoSizeSpin.value()
        self.infoSizeSpin.setSuffix(self.infos["sizemode"])
        self.infoNameEdit.setText(self.infos["name"])
        self.infoAddress.setText(self.infos["address"])
        self.infoDateCreate.setDateTime(self.infos["datecreate"])
        self.infoDateModify.setDateTime(self.infos["datemodify"])
        self.infoDateAccess.setDateTime(self.infos["dateaccess"])
        self.infoDateInsert.setDateTime(self.infos["dateinsert"])
        
        if self.infos["type"] == "book":
            self.infoTypeCombo.setCurrentIndex(0)
            self.detailBookAuthor.setText(self.infos["author"])
            self.detailBookImprintInfo.setText(self.infos["imprintinfo"])
            self.detailBookCallNumber.setText(self.infos["callnumber"])
            self.detailBookPageSpin.setValue(self.infos["page"])
            self.detailBookYearSpin.setValue(self.infos["year"])
            
        elif self.infos["type"] == "ebook":
            self.infoTypeCombo.setCurrentIndex(1)
            self.detailEbookAuthor.setText(self.infos["author"])
            self.detailEbookTitle.setText(self.infos["title"])
            self.detailEbookPageSpin.setValue(self.infos["page"])
            self.detailEbookYearSpin.setValue(self.infos["year"])
            
        elif self.infos["type"] == "image":
            self.infoTypeCombo.setCurrentIndex(2)
            self.detailImageHeightSpin.setValue(self.infos["height"])
            self.detailImageWidthSpin.setValue(self.infos["width"])
            
        elif self.infos["type"] == "music":
            self.infoTypeCombo.setCurrentIndex(3)
            self.detailMusicTitle.setText(self.infos["title"])
            self.detailMusicArtist.setText(self.infos["artist"])
            self.detailMusicAlbum.setText(self.infos["album"])
            self.detailMusicYear.setValue(self.infos["date"])
            self.detailMusicTrack.setValue(self.infos["tracknumber"])
            self.detailMusicGenre.setText(self.infos["genre"])
            self.detailMusicBitrate.setValue(self.infos["bitrate"]/1000)
            self.detailMusicSampleRate.setValue(self.infos["samplerate"])
            self.detailMusicLength.setText(str(self.infos["length"]))
            
        elif self.infos["type"] == "video":
            self.infoTypeCombo.setCurrentIndex(4)
            self.detailVideoTitle.setText(self.infos["title"])
            self.detailVideoLength.setText(str(self.infos["length"]))
            self.detailVideoHeight.setValue(self.infos["height"])
            self.detailVideoWidth.setValue(self.infos["width"])
            
        elif self.infos["type"] == "other":
            self.infoTypeCombo.setCurrentIndex(5)
            
        
    def applyAction(self):
        ddata, diff = {}, {}
        if self.new:
            self.infos = {"size":0}
            ddata["size"] = 0
        typedict = {0:"book",1:"ebook",2:"image",3:"music",4:"video",5:"other"}
        if self.type == "directory":
            ddata["name"] = str(self.dirInfoName.text())
            ddata["description"] = str(self.dirInfoDescription.toPlainText())
            ddata["datecreate"] = self.dirInfoDateCreate.dateTime().toPyDateTime()
            ddata["datemodify"] = self.dirInfoDateModify.dateTime().toPyDateTime()
            ddata["dateaccess"] = self.dirInfoDateAccess.dateTime().toPyDateTime()
            ddata["dateinsert"] = self.dirInfoDateInsert.dateTime().toPyDateTime()
            

        elif self.type == "file":
            if self.infoSizeSpin.value() != self.infos["size"]:
                size = self.infoSizeSpin.value()
                sizemode = self.infoSizeSpin.suffix()
                modes = {u" b":1,u" Kb":1024,u" Mb":1024**2,u" Gb":1024**3}
                ddata["size"] = int(size * modes[str(sizemode)])
            
            ddata["name"] = str(self.infoNameEdit.text())
            ddata["datecreate"] = self.infoDateCreate.dateTime().toPyDateTime()
            ddata["datemodify"] = self.infoDateModify.dateTime().toPyDateTime()
            ddata["dateaccess"] = self.infoDateAccess.dateTime().toPyDateTime()
            ddata["dateinsert"] = self.infoDateInsert.dateTime().toPyDateTime()
            
            ddata["type"] = typedict[self.infoTypeCombo.currentIndex()]
            
            if ddata["type"] == "book":
                ddata["author"] = str(self.detailBookAuthor.text())
                ddata["imprintinfo"] = str(self.detailBookImprintInfo.text())
                ddata["callnumber"] = str(self.detailBookCallNumber.text())
                ddata["page"] = self.detailBookPageSpin.value()
                ddata["year"] = self.detailBookYearSpin.value()
                
            elif ddata["type"] == "ebook":
                ddata["author"] = str(self.detailEBookAuthor.text())
                ddata["title"] = str(self.detailEBookTitle.text())
                ddata["page"] = self.detailEBookPageSpin.value()
                ddata["year"] = self.detailEBookYearSpin.value()
                
            elif ddata["type"] == "image":
                ddata["height"] = self.detailImageHeightSpin.value()
                ddata["width"] = self.detailImageWidthSpin.value()
                
            elif ddata["type"] == "music":
                ddata["title"] = str(self.detailMusicTitle.text())
                ddata["artist"] = str(self.detailMusicArtist.text())
                ddata["album"] = str(self.detailMusicAlbum.text())
                ddata["date"] = self.detailMusicYear.value()
                ddata["tracknumber"] = self.detailMusicTrack.value()
                ddata["genre"] = str(self.detailMusicGenre.text())
                ddata["bitrate"] = self.detailMusicBitrate.value()*1000
                ddata["samplerate"] = self.detailMusicSampleRate.value()
                ddata["length"] = int(self.detailMusicLength.text())
                
            elif ddata["type"] == "video":
                ddata["title"] = str(self.detailVideoTitle.text())
                ddata["length"] = int(self.detailVideoLength.text())
                ddata["height"] = self.detailVideoHeight.value()
                ddata["width"] = self.detailVideoWidth.value()
                    
            if not self.new and ddata["type"] != self.infos["type"]:
                oldType = self.infos["type"]
                if oldType != "other":
                    Query.setStatTrue("delete")
                    Query.setTables([libilge.typeDb[oldType]])
                    Query.setWhere([{"f_id":self.id}])
                    database.dataBase().execute(Query.returnQuery())
                    
                    oldKeys = getKeys(libilge.typeDb[oldType])
                    for i in oldKeys.keys():
                        if i != "f_id":
                            self.infos.pop(i)
                        
                newType = ddata["type"]
                newKeys = getKeys(libilge.typeDb[newType])
                for i in newKeys.keys():
                    if i != "f_id":
                        self.infos[i] = newKeys[i]
                        
                dirnow = EXP.dirNow
                EXP.chDir(id=self.upid)
                EXP.update(updated=self.infos["name"],
                           parameters={"type":ddata["type"]})
                EXP.dirNow = dirnow
                
                self.infos["type"] = ddata["type"]
        
        if self.new:
            ddata["up_id"] = self.upid
            Query.setStatTrue("select")
            Query.setSelect(["max(id)"])
            
            if self.type == "file":
                EXP.mkFile(infos=ddata)
                Query.setTables(["files"])
                
            if self.type == "directory":
                EXP.mkDir(infos=ddata)
                Query.setTables(["dirs"])
                
            self.id = database.dataBase().execute(Query.returnQuery())[0][0]
            self.new = False
            
            self.infos["name"] = ddata["name"]
            
            for i in ddata.keys():
                if not i in ["name", "size", "type", "description",
                             "datecreate","datemodify", "dateaccess",
                             "dateinsert"]:
                    diff[i] = ddata[i]
        
        else:
            for i in ddata.keys():
                if ddata[i] != self.infos[i]:
                    diff[i] = ddata[i]
        
        if len(diff.keys()) > 0:
            dirnow = EXP.dirNow
            EXP.chDir(id=self.upid)
            EXP.update(updated=self.infos["name"], parameters=diff)
            EXP.dirNow = dirnow
            
        self.parse()
    
    def setNewFileDialog(self):
        self.infoSW.setCurrentIndex(0)
        self.infoTypeCombo.setCurrentIndex(5)
        self.infoSizeSpin.setSuffix(" b")
        self.infoDateCreate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.infoDateModify.setDateTime(QtCore.QDateTime.currentDateTime())
        self.infoDateAccess.setDateTime(QtCore.QDateTime.currentDateTime())
        self.infoDateInsert.setDateTime(QtCore.QDateTime.currentDateTime())
    
    def setNewDirDialog(self):
        self.infoSW.setCurrentIndex(1)
        self.infoTypeCombo.setCurrentIndex(5)
        self.dirInfoDateCreate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dirInfoDateModify.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dirInfoDateAccess.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dirInfoDateInsert.setDateTime(QtCore.QDateTime.currentDateTime())
    
    def fillFileInfo(self):
        self.setCursor(QtCore.Qt.WaitCursor)
        filename = QtGui.QFileDialog.getOpenFileName()
        if filename == u"":
            return
        infos = {"up_id":self.upid}
        EXP.mkFile(address=str(filename), infos=infos)
        
        Query.setStatTrue("select")
        Query.setSelect(["max(id)"])
        Query.setTables(["files"])
        self.id = database.dataBase().execute(Query.returnQuery())[0][0]
        self.new = False
        
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.parse()
        
    def fillDirInfo(self):
        self.setCursor(QtCore.Qt.WaitCursor)
        dirname = QtGui.QFileDialog.getExistingDirectory(options = QtGui.QFileDialog.ShowDirsOnly)
        if dirname == u"":
            return
        infos = {"up_id":self.upid,"dateinsert":datetime.datetime.now()}
        EXP.mkDir(address=str(dirname), infos=infos)
        
        Query.setStatTrue("select")
        Query.setSelect(["max(id)"])
        Query.setTables(["dirs"])
        self.id = database.dataBase().execute(Query.returnQuery())[0][0]
        self.new = False
        
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.parse()
