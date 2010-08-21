#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database
import libilge
import datetime
import re
import readline #this is for history and editing line

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

parse1 = re.compile("(\w+=\"[^\"]*\")", re.IGNORECASE|re.UNICODE)
parse2 = re.compile("(\w+=\w+)", re.IGNORECASE|re.UNICODE)
parse3 = re.compile("(\"[^\"]*\")", re.IGNORECASE|re.UNICODE)
    
def parser(entry):
    command = entry.split()[0]
    entry = entry[len(command):]
    parameters = {}
    additions = []
    entry = entry.replace("'","\"")
    parsed = parse1.findall(entry)
    parsed += parse2.findall(entry)
    for i in parsed:
        key, value = i.split("=")
        value = value.replace("\"","")
        parameters[key]=value
        entry = entry.replace(i,"")
    additions += parse3.findall(entry)
    for i in additions:
        entry = entry.replace(i,"")
    additions += entry.split()
    return command, parameters, additions
    

DB = database.DB()

QUIT = False

print _("Welcome to bilge-katalog!\
\nFor helping only write 'help' an press Enter")

while QUIT == False:
    entry = raw_input(">>> ")
    entry = entry.decode('utf-8')
    command, parameters, additions = parser(entry)
    
    if command == "help":
        print _("helping information")
    
    if command == "quit":
        QUIT = True
        
    if command == "addcat":
        name = parameters["name"]
        try:
            desc = parameters["desc"]
        except:
            desc = ""
        try:
            directory = parameters["dir"]
        except:
            directory = None
        now = datetime.datetime.now()
        libilge.dirAdd2Db(directory, 0, name, now, desc, now, now, now)
        
#    if "showCatalogs" in opts:
 #       list = libilge.showDir(0)
  #      for i in list:
   #         print "  " + str(i)
            
    if command == "ls":
        list = libilge.showDir(additions[0])
        for i in list:
            print "  " + str(i)
        
#    if "delDir" in opts:
        #gerekli dizinin adından id'sine geçme falan yazılabilir
 #       dir_id = opts[1]
  #      libilge.dirDelFromDb(dir_id)

print _("Thanks for using bilge-katalog")
