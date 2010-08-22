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
    for i in parse3.findall(entry):
        value = i.replace("\"","")
        additions.append(value)
    for i in additions:
        entry = entry.replace(i,"")
    additions += entry.split()
    return command, parameters, additions
    

DB = database.DB()
EXP = libilge.explore()

QUIT = False

print _("Welcome to bilge-katalog!\
\nFor helping only write 'help' an press Enter")

while QUIT == False:
    entry = raw_input(">>> ")
    entry = entry.decode('utf-8')
    command, parameters, additions = parser(entry)
    
    if command == "help":
        print _("helping information")
    
    elif command == "quit":
        QUIT = True
        
    elif command == "addcat":
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
        
    elif command == "ls":
        try:
            id = parameters["id"]
            EXP.dirList(id)
        except KeyError:
            try:
                name = additions[0]
                EXP.dirListByName(name)
            except IndexError:
                EXP.dirList()
    
    elif command == "cd":
        try:
            id = parameters["id"]
            EXP.chDirById(id)
        except KeyError:
            try:
                name = additions[0]
                EXP.chDirByName(name)
            except IndexError:
                print "hiçbir şey"
        
    elif command == "rmdir":
        try:
            id = parameters["id"]
            libilge.dirDelFromDb(dir_id)
        except KeyError:
            try:
                name = additions[0]
                EXP.delDirByName(name)
            except IndexError:
                print "hiçbir şey"

print _("Thanks for using bilge-katalog")
