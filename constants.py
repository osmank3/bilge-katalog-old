#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import gettext

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

NAME = "Bilge-Katalog"
VERSION = "0.1"
SUMMARY = _("Cataloging application")
DESCRIPTION = _("Bilge-Katalog is cataloging file's infos for founding where is file(s).")
CORE_DEVELOPER = "Osman Karagöz"
CORE_EMAIL = "osmank3 [at] gmail.com"
LICENSE_NAME = "GPLv3"
URL = "http://github.com/osmank3/bilge-katalog"
TRANSLATORS = """\
tr : Osman Karagöz, osmank3 [at] gmail.com
"""
