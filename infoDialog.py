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
        elif self.infos["size"] < 1024*1024:
            self.infos["sizemode"] = " Kb"
            self.infos["size"] = float(self.infos["size"])/1024
        elif self.infos["size"] < 1024*1024*1024:
            self.infos["sizemode"] = " Mb"
            self.infos["size"] = float(self.infos["size"])/(1024*1024)
        elif self.infos["size"] < 1024*1024*1024*1024:
            self.infos["sizemode"] = " Gb"
            self.infos["size"] = float(self.infos["size"])/(1024*1024*1024)
        
        self.infoSizeSpin.setValue(self.infos["size"])
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
        pass # doldurulacak
