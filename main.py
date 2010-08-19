#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database
import libilge

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
    command = command.decode('utf-8')
    opts = command.split(" ")
    
    if "help" in opts:
        print _("helping information")
    
    if "quit" in opts:
        QUIT = True
        
    if "addCatalog" in opts:
        directory = opts[1]
        libilge.dirAdd2Db(directory)
        
    if "showCatalogs" in opts:
        list = libilge.showDir(0)
        for i in list:
            print "  " + i
            
    if "showDir" in opts:
        list = libilge.showDir(opts[1])
        for i in list:
            print "  " + i
        
    if "delDir" in opts:
        #gerekli dizinin adından id'sine geçme falan yazılabilir
        dir_id = opts[1]
        libilge.dirDelFromDb(dir_id)

print _("Thanks for using bilge-katalog")
