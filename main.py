#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

DB = database.DB()

QUIT = False

print _("Welcome to bilge-katalog!\
\nFor helping only write 'help' an press Enter")

while QUIT == False:
    command = raw_input(">>> ")
    
    if command == "help":
        print _("helping information")
    
    if command == "quit":
        QUIT = True
        
    if command == "addCatalog":
        pass#katalog ekleme fonksiyonu buraya


print _("Thanks for using bilge-katalog")
