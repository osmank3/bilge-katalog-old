#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
from constants import *

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

from PyQt4 import QtCore
from PyQt4 import QtGui
from uiQt_aboutdialog import Ui_aboutDialog

class aboutDialog(QtGui.QDialog, Ui_aboutDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.fillAll()
        
    def fillAll(self):
        name = """\
<b>%s %s</b><p>
%s<p>
%s"""% (NAME, VERSION, SUMMARY, DESCRIPTION)

        self.nameAndVersion.setText(name.decode("utf-8"))
        
        developers = """\
<b>Core Developer:</b><p>
  %s<p>
    %s"""% (CORE_DEVELOPER, CORE_EMAIL)
  
        self.developersText.setText(developers.decode("utf-8"))
        
        self.translatorsText.setText(TRANSLATORS.decode("utf-8"))

        licenseFile = QtCore.QFile("COPYING")
        if not licenseFile.open(QtCore.QIODevice.ReadOnly):
            license = LICENSE_NAME
        else:
            textstream = QtCore.QTextStream(licenseFile)
            textstream.setCodec("UTF-8")
            license = textstream.readAll()
        
        self.licenseText.setText(license)
        
        iconsLicense = "CC by-nc-sa\nhttp://creativecommons.org/licenses/by-nc-sa/3.0/"
        self.iconsLicenseText.setText(iconsLicense)
