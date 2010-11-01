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
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        
