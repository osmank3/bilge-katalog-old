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
from uiQt_userdialog import Ui_userDialog

class userDialog(QtGui.QDialog, Ui_userDialog):
    def __init__(self, new=False):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.idNow = None
        self.new = new
        
        if self.new:
            self.newAction
        
        #signals
        self.connect(self.fillInfosButton, QtCore.SIGNAL("clicked()"), self.setId)
        self.connect(self.fillInfosButton, QtCore.SIGNAL("clicked()"), self.enablingButtons)
        self.connect(self.spinId, QtCore.SIGNAL("valueChanged(int)"), self.enablingButtons)
        self.connect(self.applyButton, QtCore.SIGNAL("clicked()"), self.applyAction)
        self.connect(self.resetButton, QtCore.SIGNAL("clicked()"), self.fillInfos)
        self.connect(self.nextButton, QtCore.SIGNAL("clicked()"), self.nextAction)
        self.connect(self.prevButton, QtCore.SIGNAL("clicked()"), self.prevAction)
        self.connect(self.newButton, QtCore.SIGNAL("clicked()"), self.newAction)
        
    def setId(self):
        Query.setStatTrue("select")
        Query.setSelect(["max(id)"])
        Query.setTables(["users"])
        maxId = database.dataBase().execute(Query.returnQuery())[0][0]
        if self.spinId.value() <= maxId:
            self.idNow = self.spinId.value()
            self.fillInfos()
        else:
            self.spinId.setValue(self.idNow)
        
    def fillInfos(self):
        if type(self.idNow) == int:
            self.spinId.setValue(self.idNow)
            
            infos = EXP.infoUser(self.idNow, True)
            
            self.nameLine.setText(infos["name"])
            self.surnameLine.setText(infos["surname"])
            self.emailLine.setText(infos["email"])
            self.mobileLine.setText(infos["mobile"])
            self.homeLine.setText(infos["home"])
            self.workLine.setText(infos["work"])
            self.addressLine.setPlainText(infos["address"])
            
            borrow, reserve, tborrow = self.getBorrow()
            
            self.borrowLine.setPlainText(str(borrow))
            self.reserveLine.setPlainText(str(reserve))
            self.totalBorrowLine.setText(str(tborrow))
        
    def applyAction(self):
        infos = {}            
        infos["name"] = str(self.nameLine.text())
        infos["surname"] = str(self.surnameLine.text())
        infos["email"] = str(self.emailLine.text())
        infos["mobile"] = str(self.mobileLine.text())
        infos["home"] = str(self.homeLine.text())
        infos["work"] = str(self.workLine.text())
        infos["address"] = str(self.addressLine.toPlainText())
        if self.new:
            EXP.addUser(infos)
            
            Query.setStatTrue("select")
            Query.setSelect(["max(id)"])
            Query.setTables(["users"])
            self.idNow = database.dataBase().execute(Query.returnQuery())[0][0]
            
            self.spinId.setEnabled(True)
            self.fillInfosButton.setEnabled(True)
            self.new = False
        else:
            EXP.updateUser(self.idNow, infos)
        self.fillInfos()
        
    def nextAction(self):
        Query.setStatTrue("select")
        Query.setSelect(["max(id)"])
        Query.setTables(["users"])
        maxId = database.dataBase().execute(Query.returnQuery())[0][0]
        if self.idNow < maxId:
            self.idNow += 1
            self.fillInfos()
        
    def prevAction(self):
        if self.idNow > 1:
            self.idNow -= 1
            self.fillInfos()
            
    def getBorrow(self):
        borrow, reserve, tborrow= "", "", 0
        Query.setStatTrue("select")
        Query.setSelect(["kind","k_id"])
        Query.setTables(["lend"])
        Query.setWhere([{"u_id":self.idNow}, "AND", {"status":"'lended'"}])
        request = database.dataBase().execute(Query.returnQuery())
        for i in request:
            Query.setStatTrue("select")
            Query.setSelect(["name"])
            Query.setTables([i[0]])
            Query.setWhere([{"id":i[1]}])
            borrowed = database.dataBase().execute(Query.returnQuery())[0][0]
            borrow += borrowed + "\n"
            
        Query.setStatTrue("select")
        Query.setSelect(["kind","k_id"])
        Query.setTables(["lend"])
        Query.setWhere([{"u_id":self.idNow}, "AND", {"status":"'waiting'"}])
        request = database.dataBase().execute(Query.returnQuery())
        for i in request:
            Query.setStatTrue("select")
            Query.setSelect(["name"])
            Query.setTables([i[0]])
            Query.setWhere([{"id":i[1]}])
            reserved = database.dataBase().execute(Query.returnQuery())[0][0]
            reserve += reserved + "\n"
            
        Query.setStatTrue("select")
        Query.setSelect(["count(id)"])
        Query.setTables(["lend"])
        Query.setWhere([{"u_id":self.idNow}, "AND (", {"status":"'lended'"}, "OR", {"status":"'returned'"}, ")"])
        tborrow = database.dataBase().execute(Query.returnQuery())[0][0]
        
        return (borrow, reserve, tborrow)
        
    def enablingButtons(self, settedId=None):
        self.nextButton.setEnabled(False)
        self.prevButton.setEnabled(False)
        
        Query.setStatTrue("select")
        Query.setSelect(["max(id)"])
        Query.setTables(["users"])
        maxId = database.dataBase().execute(Query.returnQuery())[0][0]
        
        if self.idNow == 1:
            self.nextButton.setEnabled(True)
        elif self.idNow == maxId:
            self.prevButton.setEnabled(True)
        else:
            self.nextButton.setEnabled(True)
            self.prevButton.setEnabled(True)
            
    def newAction(self):
        self.spinId.setEnabled(False)
        self.fillInfosButton.setEnabled(False)
        
        self.nameLine.setText("")
        self.surnameLine.setText("")
        self.emailLine.setText("")
        self.mobileLine.setText("")
        self.homeLine.setText("")
        self.workLine.setText("")
        self.addressLine.setPlainText("")
        
        self.borrowLine.setPlainText("")
        self.reserveLine.setPlainText("")
        self.totalBorrowLine.setText("")
        
        self.new = True
