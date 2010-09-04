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
    address = []
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
    if '""' in additions:
        additions.remove('""')
    return command, parameters, additions
    
def addressParser(address):
    addressList = []
    if "/" in address:
        if address.find("/") == 0:
            addressList.append("/")
        parts = address.split("/")
        for i in parts:
            if i != "":
                addressList.append(i)
    return addressList

DB = database.dataBase()
EXP = libilge.explore()

QUIT = False

print _("Welcome to bilge-katalog!\
\nFor helping only write 'help' an press Enter")

while QUIT == False:
    entry = raw_input(">>> ")
    entry = entry.decode('utf-8')
    command, parameters, additions = parser(entry)
    
    #print command , parameters , additions
    
    if command == "help":
        print _("helping information")
    
    elif command == "quit":
        QUIT = True
        
    elif command == "mkcat":
        name = parameters["name"]
        desc = ""
        directory = None
        if parameters.has_key("desc"):
            desc = parameters["desc"]
        if parameters.has_key("dir"):
            directory = parameters["dir"]
        now = datetime.datetime.now()
        infos = {"name":str(name), "description":str(desc),
                 "dateinsert":now, "up_id":0 }
        EXP.mkDir(address=directory, infos=infos)
        #libilge.dirAdd2Db(directory, 0, name, now, desc, now, now, now)
            
    elif command == "mkdir":
        now = datetime.datetime.now()
        desc = ""
        name = ""
        directory = None
        if parameters.has_key("desc"):
            desc = parameters["desc"]
        if parameters.has_key("dir"):
            directory = parameters["dir"]
            infos = {"name":str(name), "desc":str(desc), "dateinsert":now}
            EXP.mkDir(address=directory, infos=infos)
        elif len(additions)>0:
            name = additions[0]
            infos = {"name":str(name), "desc":str(desc), "dateinsert":now}
            EXP.mkDir(infos=infos)
        
    elif command == "mkfile":
        now = datetime.datetime.now()
        name = ""
        address = None
        if parameters.has_key("address"):
            address = parameters["address"]
            infos = {"name":str(name), "dateinsert":now}
            EXP.mkFile(infos=infos)
        elif len(additions)>0:
            name = additions[0]
            infos = {"name":str(name), "dateinsert":now}
            EXP.mkFile(infos=infos)
        
    elif command == "ls":
        if parameters.has_key("id"):
            id = parameters["id"]
            EXP.dirList(id=id)
        elif len(additions)>0:
            name = additions[0]
            EXP.dirList(dirname=name)
        #elif len(address)>0:
         #   oldId = EXP.dirNow
          #  for i in address:
           #     EXP.chDir(dirname=i)
            #EXP.dirList()
            #EXP.chDir(id=oldId)
        else:
            EXP.dirList()
    
    elif command == "cd":
        if parameters.has_key("id"):
            id = parameters["id"]
            EXP.chDir(id=id)
        elif len(additions)>0:
            name = additions[0]
            EXP.chDir(dirname=name)
        #elif len(address)>0:
         #   for i in address:
          #      EXP.chDir(dirname=i)
        
    elif command == "rmdir":
        if parameters.has_key("id"):
            id = parameters["id"]
            EXP.delDir(id=id)
        elif len(additions)>0:
            name = additions[0]
            EXP.delDir(dirname = name)
        #elif len(address)>0:
         #   oldId = EXP.dirNow
          #  for i in address[:-1]:
           #     EXP.chDir(dirname=i)
            #EXP.delDirByName(address[-1])
            #EXP.chDir(id=oldId)
                    
    elif command == "rm":
        if parameters.has_key("id"):
            id = parameters["id"]
            DB.delFile(id=id)
        elif len(additions)>0:
            name = additions[0]
            EXP.delFile(filename=name)
        #elif len(address)>0:
         #   oldId = EXP.dirNow
          #  for i in address[:-1]:
           #     EXP.chDir(dirname=i)
            #EXP.delFileByName(address[-1])
            #EXP.chDir(id=oldId)
                
    elif command == "info":
        if len(additions)>0:
            name = additions[0]
            info = EXP.infoByName(name)
            print info
        #elif len(address)>0:
         #   oldId = EXP.dirNow
          #  for i in address[:-1]:
           #     EXP.chDir(dirname=i)
            #info = EXP.infoByName(address[-1])
            #print info
            #EXP.chDir(id=oldId)

print _("Thanks for using bilge-katalog")
