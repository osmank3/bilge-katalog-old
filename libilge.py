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
    up_id = DB.addDir(up_id=up_id, name=name, date=date, desc=desc)
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
    for i in filelist:
        DB.delFile(i)
        DB.delInfo(i)
    dirList = DB.searchDir(dir_id)
    for i in dirList:
        dirDelFromDb(i)
