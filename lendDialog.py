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
from uiQt_lenddialog import Ui_lendDialog

class lendDialog(QtGui.QDialog, Ui_lendDialog):
    def __init__(self, type, id):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.kId = id
        if type == "directory":
            self.kind = "dirs"
        elif type == "file":
            self.kind = "files"
            
        self.mbox = QtGui.QMessageBox(self)
        self.mbox.setWindowTitle(QtGui.QApplication.translate("lendDialog", "Lending", None, QtGui.QApplication.UnicodeUTF8))
        
        #signals
        self.connect(self.lendButton, QtCore.SIGNAL("clicked()"), self.lending)
        self.connect(self.reserveButton, QtCore.SIGNAL("clicked()"), self.lendToReserved)
        self.connect(self.idLine, QtCore.SIGNAL("textChanged(QString)"), self.setLendButtonStatus)
        
    def setLendButtonStatus(self, string):
        if string == "":
            self.lendButton.setEnabled(False)
            self.uid = None
        else:
            self.lendButton.setEnabled(True)
            try:
                self.uid = int(self.idLine.text())
                Query.setStatTrue("select")
                Query.setSelect(["max(id)"])
                Query.setTables(["users"])
                maxId = database.dataBase().execute(Query.returnQuery())[0][0]
                if self.uid < 1 or self.uid > maxId:
                    self.uid = None
                    self.idLine.clear()
            except:
                self.uid = None
                self.idLine.clear()
        
    def lending(self):
        if self.uid != None:
            Query.setStatTrue("select")
            Query.setTables(["lend"])
            Query.setSelect(["*"])
            Query.setWhere([{"kind":"'%s'"% self.kind}, "AND",
                            {"k_id":self.kId}, "AND", {"status":"'lended'"}])
            request = database.dataBase().execute(Query.returnQuery())
            if len(request)>0:
                box = QtGui.QMessageBox.question(self,
                        QtGui.QApplication.translate("lendDialog", "Lending",
                                None, QtGui.QApplication.UnicodeUTF8),
                        QtGui.QApplication.translate("lendDialog",
                                "That object is borrowed.\n" + \
                                "Are you want to reserve it?", None,
                                QtGui.QApplication.UnicodeUTF8),
                        QtGui.QApplication.translate("lendDialog", "Yes",
                                None, QtGui.QApplication.UnicodeUTF8),
                        QtGui.QApplication.translate("lendDialog", "No",
                                None, QtGui.QApplication.UnicodeUTF8))
                if box == 0:
                    self.reserve()
                else:
                    pass
            else:
                self.getReserveList()
                if len(self.reserveList)>0:
                    if self.uid != self.reserveList[0]:
                        box = QtGui.QMessageBox.question(self,
                                QtGui.QApplication.translate("lendDialog",
                                        "Lending", None,
                                        QtGui.QApplication.UnicodeUTF8),
                                QtGui.QApplication.translate("lendDialog",
                                        "Wait for the order!\n" + \
                                        "Are you want to reserve it?",
                                        None, QtGui.QApplication.UnicodeUTF8),
                                QtGui.QApplication.translate("lendDialog",
                                        "Yes", None,
                                        QtGui.QApplication.UnicodeUTF8),
                                QtGui.QApplication.translate("lendDialog",
                                        "No", None,
                                        QtGui.QApplication.UnicodeUTF8))
                        if box == 0:
                            self.reserve()
                        else:
                            pass
                    else:
                        self.lendToReserved()
                else:
                    Query.setStatTrue("insert")
                    Query.setTables(["lend"])
                    Query.setKeys(["kind", "k_id", "u_id", "lenddate",
                                   "extension", "status"])
                    Query.setValues([self.kind, self.kId, self.uid,
                                     datetime.datetime.now(), 0, "lended"])
                    database.dataBase().execute(Query.returnQuery())
                    self.close()
                    
    def reserve(self):
        Query.setStatTrue("insert")
        Query.setTables(["lend"])
        Query.setKeys(["kind", "k_id", "u_id", "status"])
        Query.setValues([self.kind, self.kId, self.uid, "waiting"])
        database.dataBase().execute(Query.returnQuery())
        self.close()
        
    def getReserveList(self):
        self.reserveList = []
        
        Query.setStatTrue("select")
        Query.setSelect(["u_id"])
        Query.setTables(["lend"])
        Query.setWhere([{"kind":"'%s'"% self.kind}, "AND", {"k_id":self.kId},
                         "AND", {"status":"'waiting'"}])
        Query.setAppendix("ORDER BY id")
        request = database.dataBase().execute(Query.returnQuery())        
        for i in request:
            self.reserveList.append(i[0])
            
    def lendToReserved(self):
        Query.setStatTrue("select")
        Query.setTables(["lend"])
        Query.setSelect(["*"])
        Query.setWhere([{"kind":"'%s'"% self.kind}, "AND", {"k_id":self.kId},
                         "AND", {"status":"'lended'"}])
        request = database.dataBase().execute(Query.returnQuery())
        if len(request)>0:
            box = QtGui.QMessageBox.information(self,
                    QtGui.QApplication.translate("lendDialog", "Lending",
                            None, QtGui.QApplication.UnicodeUTF8),
                    QtGui.QApplication.translate("lendDialog",
                            "That object is borrowed.", None,
                            QtGui.QApplication.UnicodeUTF8),
                    QtGui.QApplication.translate("lendDialog", "Ok", None,
                            QtGui.QApplication.UnicodeUTF8))
        else:
            self.getReserveList()
            if len(self.reserveList) == 0:
                box = QtGui.QMessageBox.information(self,
                        QtGui.QApplication.translate("lendDialog", "Lending",
                                None, QtGui.QApplication.UnicodeUTF8),
                        QtGui.QApplication.translate("lendDialog",
                                "Object does not reserved to anybody", None,
                                QtGui.QApplication.UnicodeUTF8),
                        QtGui.QApplication.translate("lendDialog", "Ok", None,
                                QtGui.QApplication.UnicodeUTF8))
            else:
                self.uid = self.reserveList[0]
                Query.setStatTrue("update")
                Query.setTables(["lend"])
                Query.setSet({"lenddate":datetime.datetime.now(),
                              "extension":0,
                              "status":"lended"})
                Query.setWhere([{"kind":"'%s'"% self.kind}, "AND",
                                {"k_id":self.kId}, "AND",
                                {"status":"'waiting'"}, "AND",
                                {"u_id":self.uid}])
                database.dataBase().execute(Query.returnQuery())
                self.close()
