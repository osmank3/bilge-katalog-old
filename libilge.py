#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database
import datetime

now = datetime.datetime.now

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

DB = database.DB()

def dirAdd2Db(directory, up_id, name, datei, desc, datec, datem, datea):
    up_id = DB.addDir(up_id, name, datec, datem, datea, datei, desc)
    inDir = os.listdir(directory)
    if len(inDir)>0:
        for i in inDir:
            dirI = directory + os.sep + i
            
            stat = os.stat(dirI)
            size = stat.st_size
            datec = datetime.datetime.fromtimestamp(stat.st_ctime)
            datem = datetime.datetime.fromtimestamp(stat.st_mtime)
            datea = datetime.datetime.fromtimestamp(stat.st_atime)
            
            if os.path.isdir(dirI):
                dirAdd2Db(dirI, up_id, i, datei, "", datec, datem, datea)
            else:
                type="text"#buraya doğru hali girilmeli
                DB.addFile(up_id, i, size, datec, datem, datea, datei, type)
    
def dirDelFromDb(dir_id):
    DB.delDir(dir_id)
    fileList = DB.searchFile(dir_id)
    for i in fileList:
        DB.delFile(i)
        #DB.delInfo(i)
    dirList = DB.searchDir(dir_id)
    for i in dirList:
        dirDelFromDb(i)
        
def showDir(id, hide=True):
    dirs, files = DB.listDir(id) #dir->{name:id}
    list = []
    for i in dirs.keys():
        if type(i) == type(0) or i[0] != '.':
            list.append(i)
        elif hide == False:
            list.append(i)
    for i in files.keys():
        if type(i) == type(0) or i[0] != '.':
            list.append(i)
        elif hide == False:
            list.append(i)
    list.sort()
    return list
    rows, columns = os.popen("stty size", "r").read().split()
    maxleight=0
    for i in list:
        if maxleight<len(i):
            maxleight = len(i)
    for i in list:
        if len(i)<maxleight:
            number = list.index(i)
            while len(i) == maxleight:
                i += " "
            list[number] = i
    
    
    
    
    
# Colored printing

def clr_blue(text):
    return "\033[94m" + text + "\033[0m"
def clr_no(text):
    return "\033[0m" + text + "\033[0m"
def clr_yellow(text):
    return "\033[93m" + text + "\033[0m"
