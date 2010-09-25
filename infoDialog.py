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
    def __init__(self, type, id, upid):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.type = type
        self.id = id
        self.upid = upid
        
        # signals
        self.connect(self.resetButton, QtCore.SIGNAL("clicked()"), self.parse)
        self.connect(self.applyButton, QtCore.SIGNAL("clicked()"), self.applyAction)
        
        self.parse()
        
    def parse(self):
        if self.type == u"directory":
            self.dirInfos()
            
        elif self.type == "file":
            self.fileInfos()
            
    def dirInfos(self):
        self.infoTypeCombo.setCurrentIndex(5) #self.detailSW.setCurrentIndex(5)
        self.infoSW.setCurrentIndex(1) # infoSW 0, 1 = fileInfo, DirectoryInfo
        
        self.infos = EXP.info(id=self.id, type=TYPES[str(self.type)], redict=True)
        
        self.dirInfoName.setText(self.infos["name"])
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
        self.infoDateCreate.setDateTime(self.infos["datecreate"])
        self.infoDateModify.setDateTime(self.infos["datemodify"])
        self.infoDateAccess.setDateTime(self.infos["dateaccess"])
        self.infoDateInsert.setDateTime(self.infos["dateinsert"])
        
        if self.infos["type"] == "book":
            self.infoTypeCombo.setCurrentIndex(0)
            self.detailBookAuthor.setText(self.infos["author"])
            self.detailBookImprintInfo.setText(self.infos["imprintinfo"])
            self.detailBookCallNuber.setText(self.infos["callnumber"])
            self.detailBookPageSpin.setValue(self.infos["page"])
            self.detailBookYearSpin.setValue(self.infos["year"])
            
        elif self.infos["type"] == "ebook":
            self.infoTypeCombo.setCurrentIndex(1)
            self.detailEBookAuthor.setText(self.infos["author"])
            self.detailEBookTitle.setText(self.infos["title"])
            self.detailEBookPageSpin.setValue(self.infos["page"])
            self.detailEBookYearSpin.setValue(self.infos["year"])
            
        elif self.infos["type"] == "image":
            self.infoTypeCombo.setCurrentIndex(2)
            self.detailImageCreateDate.setDateTime(self.infos["datecreate"])
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
        typedict = {0:"book",1:"ebook",2:"image",3:"music",4:"video",5:"other"}
        if self.type == "directory":
            ddata["name"] = str(self.dirInfoName.text())
            ddata["description"] = str(self.dirInfoDescription.toPlainText())
            ddata["datecreate"] = self.dirInfoDateCreate.dateTime()
            ddata["datemodify"] = self.dirInfoDateModify.dateTime()
            ddata["dateaccess"] = self.dirInfoDateAccess.dateTime()
            ddata["dateinsert"] = self.dirInfoDateInsert.dateTime()
            

        elif self.type == "file":
            if self.infoSizeSpin.value() != self.infos["size"]:
                size = self.infoSizeSpin.value()
                sizemode = self.infoSizeSpin.suffix()
                modes = {u" b":1,u" Kb":1024,u" Mb":1024**2,u" Gb":1024**3}
                ddata["size"] = int(size * modes[str(sizemode)])
            
            ddata["name"] = self.infoNameEdit.text()
            ddata["datecreate"] = self.infoDateCreate.dateTime()
            ddata["datemodify"] = self.infoDateModify.dateTime()
            ddata["dateaccess"] = self.infoDateAccess.dateTime()
            ddata["dateinsert"] = self.infoDateInsert.dateTime()
            
            ddata["type"] = typedict[self.infoTypeCombo.currentIndex()]
            
            if ddata["type"] == "book":
                ddata["author"] = self.detailBookAuthor.text()
                ddata["imprintinfo"] = self.detailBookImprintInfo.text()
                ddata["callnumber"] = self.detailBookCallNuber.text()
                ddata["page"] = self.detailBookPageSpin.value()
                ddata["year"] = self.detailBookYearSpin.value()
                
            elif ddata["type"] == "ebook":
                ddata["author"] = self.detailEBookAuthor.text()
                ddata["title"] = self.detailEBookTitle.text()
                ddata["page"] = self.detailEBookPageSpin.value()
                ddata["year"] = self.detailEBookYearSpin.value()
                
            elif ddata["type"] == "image":
                ddata["datecreate"] = self.detailImageCreateDate.dateTime()
                ddata["height"] = self.detailImageHeightSpin.value()
                ddata["width"] = self.detailImageWidthSpin.value()
                
            elif ddata["type"] == "music":
                ddata["title"] = self.detailMusicTitle.text()
                ddata["artist"] = self.detailMusicArtist.text()
                ddata["album"] = self.detailMusicAlbum.text()
                ddata["date"] = self.detailMusicYear.value()
                ddata["tracknumber"] = self.detailMusicTrack.value()
                ddata["genre"] = self.detailMusicGenre.text()
                ddata["bitrate"] = self.detailMusicBitrate.value()*1000
                ddata["samplerate"] = self.detailMusicSampleRate.value()
                ddata["length"] = int(self.detailMusicLength.text())
                
            elif ddata["type"] == "video":
                ddata["title"] = self.detailVideoTitle.text()
                ddata["length"] = int(self.detailVideoLength.text())
                ddata["height"] = self.detailVideoHeight.value()
                ddata["width"] = self.detailVideoWidth.value()
                    
            #if ddata["type"] != infos["type"]:
                #burada infos["type"]'daki ayrıntı verileri silinmeli.
                
        for i in ddata.keys():
            if ddata[i] != self.infos[i]:
                diff[i] = ddata[i]
        
        if len(diff.keys()) > 0:
            dirnow = EXP.dirNow
            EXP.chDir(id=self.upid)
            EXP.update(updated=self.infos["name"], parameters=diff)
            EXP.dirNow = dirnow
            
            self.parse()
