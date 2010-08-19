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

def dirAdd2Db(directory, up_id=0, name='', date='', desc=''):
    up_id = DB.addDir(up_id, name, date, desc)
    inDir = os.listdir(directory)
    if len(inDir)>0:
        for i in inDir:
            dirI = directory + os.sep + i
            if os.path.isdir(dirI):
                dirAdd2Db(dirI, up_id, i, date, desc)
            else:
                size=0;type="text"#buraya doğru halleri girilmeli
                DB.addFile(up_id, i, size, date, type)
    
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
    dirs, files = DB.showDir(id) #dir->{id:name}
    list = []
    for i in dirs.values():
        if i[0] != '.':
            list.append(clr_blue(i))
        elif hide == False:
            list.append(clr_blue(i))
    for i in files.values():
        if i[0] != '.':
            list.append(clr_yellow(i))
        elif hide == False:
            list.append(clr_yellow(i))
    return list
    
# Colored printing

def clr_blue(text):
    return "\033[94m" + text + "\033[0m"
def clr_no(text):
    return "\033[0m" + text + "\033[0m"
def clr_yellow(text):
    return "\033[93m" + text + "\033[0m"
