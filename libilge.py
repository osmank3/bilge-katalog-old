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

types={ ".aac":"music", ".acc":"music", ".mp3":"music", ".ogg":"music",
        ".jpg":"image", ".png":"image", ".bmp":"image", "jpeg":"image",
        ".avi":"video", "mpeg":"video", ".mp4":"video", ".flv":"video",
        ".pdf":"ebook", "book":"book"}

DB = database.DB()

def dirAdd2Db(directory, up_id, name, datei, desc, datec, datem, datea):
    up_id = DB.addDir(up_id, name, datec, datem, datea, datei, desc)
    if directory == None:
        return
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
                try:
                    type=types[i[-4:]]
                except:
                    type="other"
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
        
class explore:
    def __init__(self):
        self.dirNow = 0
        self.listDir = []
        self.hide = True
        
    def dirList(self, id=None):
        if id:
            dirs, files = DB.listDirById(id)
        else:
            dirs, files = DB.listDirById(self.dirNow)
        self.listDir = []
        for i in dirs.keys() + files.keys():
            if type(i) == type(0) or i[0] != '.':
                self.listDir.append(i)
            elif hide == False:
                self.listDir.append(i)
        self.show()
        
    def dirListByName(self, dirname):
        if dirname == "/":
            dirs = {"/":0}
        else:
            dirs, files = DB.listDirById(self.dirNow)
        try:
            dirs, files = DB.listDirById(dirs[dirname])
            self.listDir = []
            for i in dirs.keys() + files.keys():
                if type(i) == type(0) or i[0] != '.':
                    self.listDir.append(i)
                elif hide == False:
                    self.listDir.append(i)
            self.show()
        except KeyError:
            print _("%s is not a directory"% dirname)
        
    def chDirByName(self, dirname):
        if dirname == "/":
            dirs = {"/":0}
        elif dirname == "..":
            if self.dirNow != 0:
                id = DB.takeDirUpId(self.dirNow)
                dirs = {"..":id}
            else:
                dirs = {"..":0}
        else:
            dirs, files = DB.listDirById(self.dirNow)
        try:
            self.dirNow = dirs[dirname]
        except KeyError:
            print _("%s is not a directory"% dirname)
            
    def chDirById(self, id):
        self.dirNow = id
        
    def delDirByName(self, dirname):
        if dirname == "/":
            dirs = {"/":0}
            self.dirNow = 0
        else:
            dirs, files = DB.listDirById(self.dirNow)
        try:
            dirDelFromDb(dirs[dirname])
        except KeyError:
            print _("%s is not a directory"% dirname)
        
    def show(self):
        self.listDir.sort()
        for i in self.listDir:
            print i



# Colored printing

def clr_blue(text):
    return "\033[94m" + text + "\033[0m"
def clr_no(text):
    return "\033[0m" + text + "\033[0m"
def clr_yellow(text):
    return "\033[93m" + text + "\033[0m"
    
# testing codes
def test():
    #şimdilik buradan sonrası deneme amaçlı kalsın...
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
