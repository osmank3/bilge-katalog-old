#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database
import datetime
import detailer

#now = datetime.datetime.now

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
                infos = {}
                if types.has_key(i[-4:].lower()):
                    type=types[i[-4:].lower()]
                    infos = tagging(dirI, i[-4:].lower())
                else:
                    type="other"
                f_id = DB.addFile(up_id, i, size, datec, datem, datea, datei, type)
                if len(infos.keys())>0:
                    infos2Db(f_id, infos, type)

                    
def infos2Db(f_id, infos, type):
    if type == "music":
        title = infos["title"]
        artist = infos["artist"]
        album = infos["album"]
        date = infos["date"]
        tracknumber = infos["tracknumber"]
        genre = infos["genre"]
        bitrate = infos["bitrate"]
        frequence = infos["frequence"]
        length = infos["length"]
        DB.addMusic(f_id, title, artist, album, date, tracknumber, genre, bitrate, frequence, length)
                        
        
def tagging(address, type):
    if type == ".mp3":
        infos = detailer.mp3Tags(address)
        return infos
    elif type == ".ogg":
        infos = detailer.oggTags(address)
        return infos
    
def dirDelFromDb(dir_id):
    DB.delDir(dir_id)
    dirs, files = DB.listDirById(dir_id)
    for i in files.values():
        type = DB.delFile(i)
        DB.delInfo(i, type)
    for i in dirs.values():
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
            if type(i) == type(0) or i.find(".") != 0:
                self.listDir.append(i)
            elif self.hide == False:
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
                if type(i) == type(0) or i.find(".") != 0:
                    self.listDir.append(i)
                elif self.hide == False:
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

    def delFileByName(self, filename):
        dirs, files = DB.listDirById(self.dirNow)
        try:
            type = DB.delFile(files[filename])
            DB.delInfo(files[filename], type)
        except KeyError:
            print _("%s is not a file"% filename)
        
    def show(self):
        self.listDir.sort()
        for i in self.listDir:
            print i
            
    def infoById(self, id, type):
        if id != 0:
            infos = DB.info(id, type)
            text = ""
            if type == "dirs":
                text += _("Name")       +   "\t: %s\n"% infos["name"]
                text += _("Address")    +   "\t: %s\n"% infos["up_id"]
                text += _("Descrition") +   "\t: %s\n"% infos["description"]
                text += _("Create Date")+   "\t: %s\n"% infos["datecreate"]
                text += _("Modify Date")+   "\t: %s\n"% infos["datemodify"]
                text += _("Access Date")+   "\t: %s\n"% infos["dateaccess"]
                text += _("Cataloging Date")+"\t: %s"% infos["dateaddcat"]
                
            elif type == "files":
                text += _("Name")       +   "\t: %s\n"% infos["name"]
                text += _("Address")    +   "\t: %s\n"% infos["up_id"]
                text += _("Size")       +   "\t: %s\n"% infos["size"]
                text += _("Type")       +   "\t: %s\n"% infos["type"]
                text += _("Create Date")+   "\t: %s\n"% infos["datecreate"]
                text += _("Modify Date")+   "\t: %s\n"% infos["datemodify"]
                text += _("Access Date")+   "\t: %s\n"% infos["dateaccess"]
                text += _("Cataloging Date")+ "\t: %s"% infos["dateaddcat"]
                
            return text
            
    def infoByName(self, name):
        dirs, files = DB.listDirById(self.dirNow)
        info = ""
        if name in dirs.keys():
            info = self.infoById(dirs[name], "dirs")
        elif name in files.keys():
            info = self.infoById(files[name], "files")
        return info
        
    def mkdir(self, directory, name, desc, date):
        if directory != None:
            name = os.path.split(directory)[-1]
            if name == "":
                name = os.path.split(os.path.split(directory)[0])[-1]
        dirAdd2Db(directory, self.dirNow, name, date, desc, date, date, date)

    def mkfile(self, address, name, datei):
        size = 0
        datec = datei
        datem = datei
        datea = datei
        infos = {}
        if address != None:
            name = os.path.split(address)[-1]
            if name == "":
                name = os.path.split(os.path.split(address)[0])[-1]
            stat = os.stat(address)
            size = stat.st_size
            datec = datetime.datetime.fromtimestamp(stat.st_ctime)
            datem = datetime.datetime.fromtimestamp(stat.st_mtime)
            datea = datetime.datetime.fromtimestamp(stat.st_atime)
        if types.has_key(name[-4:].lower()):
            type=types[name[-4:].lower()]
            infos = tagging(address, name[-4:].lower())
        else:
            type="other"
        f_id = DB.addFile(self.dirNow, name, size, datec, datem, datea, datei, type)
        if len(infos.keys())>0:
            infos2Db(f_id, infos, type)


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
