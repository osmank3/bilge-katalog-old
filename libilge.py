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

types = {   ".aac":"music", ".acc":"music", ".mp3":"music", ".ogg":"music",
            ".jpg":"image", ".png":"image", ".bmp":"image", "jpeg":"image",
            ".avi":"video", "mpeg":"video", ".mp4":"video", ".flv":"video",
            ".pdf":"ebook", "book":"book"}
typeDb = {  "book":"binfo", "ebook":"einfo", "image":"iinfo",
            "music":"minfo", "video":"vinfo"}

TransKeys = {   "name"          :   _("Name"),
                "address"       :   _("Address"),
                "datecreate"    :   _("Create Date"),
                "datemodify"    :   _("Modify Date"),
                "dateaccess"    :   _("Access Date"),
                "dateinsert"    :   _("Cataloging Date"),
                "description"   :   _("Description"),
                "size"          :   _("Size"),
                "type"          :   _("Type"),
                "title"         :   _("Title"),
                "artist"        :   _("Artist"),
                "album"         :   _("Album"),
                "date"          :   _("Year"),
                "tracknumber"   :   _("Track"),
                "genre"         :   _("Genre"),
                "bitrate"       :   _("Bitrate"),
                "samplerate"    :   _("Sample Rate"),
                "length"        :   _("Length"),
                "author"        :   _("Author"),
                "imprintinfo"   :   _("Imprint Info"),
                "callnumber"    :   _("Call Number"),
                "year"          :   _("Year"),
                "page"          :   _("Page"),
                "width"         :   _("Width"),
                "height"        :   _("Height")    }

KeysQuene = [   "name", "address", "size", "type", "description", "title",
                "artist", "album", "date", "tracknumber", "genre", "bitrate",
                "samplerate", "length", "author", "page", "year",
                "callnumber", "imprintinfo", "width", "height", "datecreate",
                "datemodify", "dateaccess", "dateinsert"]

DB = database.dataBase()

def tagging(address, type):
    if types[type] == "image":
        infos = detailer.imageInfo(address)
        return infos
    elif types[type] == "video":
        infos = detailer.videoInfo(address)
        return infos
    elif type == ".mp3":
        infos = detailer.mp3Tags(address)
        return infos
    elif type == ".ogg":
        infos = detailer.oggTags(address)
        return infos
    
class explore:
    def __init__(self):
        self.dirNow = 0
        self.listDir = []
        self.hide = True
        self.query = database.EditQuery()
        
    def mkDir(self, address=None, infos={}):
        values = []
        keys = []
        if not infos.has_key("up_id"):
            infos["up_id"] = self.dirNow
        datei = infos["dateinsert"]
        if infos["up_id"] == 0:
            infos["datecreate"] = datei
            infos["datemodify"] = datei
            infos["dateaccess"] = datei
        self.query.setStatTrue("pragma")
        self.query.setTables(["dirs"])
        request = DB.execute(self.query.returnQuery())
        for i in request:
            if i[1] != "id":
                keys.append(i[1])
                try:
                    values.append( infos[i[1]] )
                except KeyError:
                    values.append("")
        
        self.query.setStatTrue("insert")
        self.query.setTables(["dirs"])
        self.query.setKeys(keys)
        self.query.setValues(values)
        DB.execute(self.query.returnQuery())
        
        self.query.setStatTrue("select")
        self.query.setSelect(["max(id)"])
        self.query.setTables(["dirs"])
        upId = DB.execute(self.query.returnQuery())[0][0]
        
        if address:
            ListDir = os.listdir(address)
            if len(ListDir)>0:
                for i in ListDir:
                    addrI = address + os.sep + i
                    
                    infos = {}
                    infos["name"] = i
                    infos["up_id"] = upId
                    
                    stat = os.stat(addrI)
                    infos["size"] = int(stat.st_size)
                    infos["datecreate"] = datetime.datetime.fromtimestamp(stat.st_ctime)
                    infos["datemodify"] = datetime.datetime.fromtimestamp(stat.st_mtime)
                    infos["dateaccess"] = datetime.datetime.fromtimestamp(stat.st_atime)
                    infos["dateinsert"] = datei
                    
                    if os.path.isdir(addrI):
                        self.mkDir(addrI, infos)
                    else:
                        self.mkFile(addrI, infos)
                    
    def mkFile(self, address=None, infos={}):
        if address != None:
            infos["name"] = os.path.split(address)[-1]
            if infos["name"] == "":
                infos["name"] = os.path.split(os.path.split(address)[0])[-1]
            stat = os.stat(address)
            infos["size"] = int(stat.st_size)
            infos["datecreate"] = datetime.datetime.fromtimestamp(stat.st_ctime)
            infos["datemodify"] = datetime.datetime.fromtimestamp(stat.st_mtime)
            infos["dateaccess"] = datetime.datetime.fromtimestamp(stat.st_atime)
            infos["dateinsert"] = datetime.datetime.now()
        
        elif not infos.has_key("up_id"):
            infos["up_id"] = self.dirNow
            
        name = infos["name"]
        if types.has_key(name[-4:].lower()):
            infos["type"] = types[name[-4:].lower()]
            if address:
                details = tagging(address, name[-4:].lower())
            else:
                details = None
        else:
            details = None
            infos["type"]="other"
        
        values = []
        keys = []
        self.query.setStatTrue("pragma")
        self.query.setTables(["files"])
        request = DB.execute(self.query.returnQuery())
        for i in request:
            if i[1] != "id":
                keys.append(i[1])
                try:
                    values.append( infos[i[1]] )
                except KeyError:
                    values.append("")
        
        self.query.setStatTrue("insert")
        self.query.setKeys(keys)
        self.query.setValues(values)
        self.query.setTables(["files"])
        DB.execute(self.query.returnQuery())
        
        if details:
            self.query.setStatTrue("select")
            self.query.setSelect(["max(id)"])
            self.query.setTables(["files"])
            fId = DB.execute(self.query.returnQuery())[0][0]
            details["f_id"] = fId
            
            detValues = []
            detKeys = []
            self.query.setStatTrue("pragma")
            self.query.setTables([typeDb[infos["type"]]])
            request = DB.execute(self.query.returnQuery())
            for i in request:
                detKeys.append(i[1])
                try:
                    detValues.append( details[i[1]] )
                except KeyError:
                    detValues.append("")
            
            self.query.setStatTrue("insert")
            self.query.setKeys(detKeys)
            self.query.setValues(detValues)
            self.query.setTables([typeDb[infos["type"]]])
            DB.execute(self.query.returnQuery())
        
        
    def dirList(self, id=None, dirname=None):
        if id == None:
            id = self.dirNow
        if dirname and "/" in dirname:
            id = 0
        dirs, files = {}, {}
        self.query.setStatTrue("select")
        self.query.setSelect(["id", "name"])
        self.query.setTables(["dirs"])
        self.query.setWhere([{"up_id":id}])
        Dirs = DB.execute(self.query.returnQuery())
        for i in Dirs:
            dirs[i[1]]=i[0]
        self.query.setTables(["files"])
        Files = DB.execute(self.query.returnQuery())
        for i in Files:
            files[i[1]]=i[0]
            
        if dirname and "/" not in dirname:
            try:
                self.dirList(id=dirs[dirname])
            except KeyError:
                print _("%s is not a directory"% dirname)
        
        else:
            self.listDir = []
            for i in dirs.keys() + files.keys():
                if type(i) == type(0) or i.find(".") != 0:
                    self.listDir.append(i)
                elif self.hide == False:
                    self.listDir.append(i)
            self.show()
        
    def chDir(self, id=None, dirname=None):
        if id:
            self.dirNow = id
        elif dirname:
            if dirname == "/":
                self.dirNow = 0
            elif dirname == "..":
                if self.dirNow != 0:
                    self.query.setStatTrue("select")
                    self.query.setSelect(["up_id"])
                    self.query.setTables(["dirs"])
                    self.query.setWhere([{"id":self.dirNow}])
                    up_id = DB.execute(self.query.returnQuery())[0][0]
                    self.dirNow = up_id
            else:
                dirs = {}
                self.query.setStatTrue("select")
                self.query.setSelect(["id", "name"])
                self.query.setTables(["dirs"])
                self.query.setWhere([{"up_id":self.dirNow}])
                Dirs = DB.execute(self.query.returnQuery())
                for i in Dirs:
                    dirs[i[1]]=i[0]                    
                try:
                    self.dirNow = dirs[dirname]
                except KeyError:
                    print _("%s is not a directory"% dirname)
            
    def delDir(self, id=None, dirname=None):
        dirs = {}
        if dirname and dirname != "/":
            self.query.setStatTrue("select")
            self.query.setSelect(["id", "name"])
            self.query.setTables(["dirs"])
            self.query.setWhere([{"up_id":self.dirNow}])
            Dirs = DB.execute(self.query.returnQuery())
            for i in Dirs:
                dirs[i[1]]=i[0]
            try:
                id = dirs[dirname]
            except KeyError:
                print _("%s is not a directory"% dirname)
        elif dirname and dirname == "/":
            id = 0
        elif id:
            id = id  # Is this joke? :D Yes
        else:
            return False
        self.query.setStatTrue("delete")
        self.query.setTables(["dirs"])
        self.query.setWhere([{"id":id}])
        DB.execute(self.query.returnQuery()) #delete directory
        
        self.query.setStatTrue("select")
        self.query.setSelect(["id"])
        self.query.setTables(["files"])
        self.query.setWhere([{"up_id":id}])
        request = DB.execute(self.query.returnQuery())
        for i in request:
            self.delFile(id=i[0]) #delete files in deleted directory
        
        self.query.setStatTrue("select")
        self.query.setSelect(["id"])
        self.query.setTables(["dirs"])
        self.query.setWhere([{"up_id":id}])
        Dirs = DB.execute(self.query.returnQuery())
        for i in Dirs:
            self.delDir(id=i[0])

    def delFile(self, id=None, filename=None):
        if filename:
            files = {}
            self.query.setStatTrue("select")
            self.query.setSelect(["id", "name", "type"])
            self.query.setTables(["files"])
            self.query.setWhere([{"up_id":self.dirNow}])
            Files = DB.execute(self.query.returnQuery())
            for i in Files:
                files[i[1]]=[i[0], i[2]]
            try:
                id, type = files(filename)
            except KeyError:
                print _("%s is not a file"% filename)
        elif id:
            self.query.setStatTrue("select")
            self.query.setSelect(["type"])
            self.query.setTables(["files"])
            self.query.setWhere([{"id":id}])
            request = DB.execute(self.query.returnQuery())
            type = request[0][0]
        
        if id:
            self.query.setStatTrue("delete")
            self.query.setTables(["files"])
            self.query.setWhere([{"id":id}])
            DB.execute(self.query.returnQuery()) # delete file
            
            if type != "other":
                self.query.setTables([typeDb[type]])
                self.query.setWhere([{"f_id":id}])
                DB.execute(self.query.returnQuery()) # delete file detail info
        
    def show(self):
        self.listDir.sort()
        for i in self.listDir:
            print i

    def genAddress(self, up_id):
        upDirs = []
        address = "/"
        while up_id != 0:
            self.query.setStatTrue("select")
            self.query.setSelect(["up_id","name"])
            self.query.setTables(["dirs"])
            self.query.setWhere([{"id":up_id}])
            request = DB.execute(self.query.returnQuery())
            up_id, name = request[0]
            upDirs.append(name)
        upDirs.reverse()
        for i in upDirs:
            address += i + "/"
        return address
            
    def info(self, id=None, name=None, type=None):
        if name:
            self.query.setStatTrue("select")
            self.query.setSelect(["name, id"])
            self.query.setTables(["dirs"])
            self.query.setWhere([{"up_id":self.dirNow}])
            Dirs = DB.execute(self.query.returnQuery())
            for i in Dirs:
                if i[0] == name:
                    id = i[1]
                    type = "dirs"
            self.query.setTables(["files"])
            Files = DB.execute(self.query.returnQuery())
            for i in Files:
                if i[0] == name:
                    id = i[1]
                    type = "files"
        if id and type:
            self.query.setStatTrue("pragma")
            self.query.setTables([type])
            keys = DB.execute(self.query.returnQuery())
            
            self.query.setStatTrue("select")
            self.query.setSelect(["*"])
            self.query.setTables([type])
            self.query.setWhere([{"id":id}])
            values = DB.execute(self.query.returnQuery())
            
            infos = {}
            n = 0
            while n<len(keys):
                if keys[n][1] != "id" and keys[n][1] != "up_id":
                    infos[keys[n][1]] = values[0][n]
                if keys[n][1] == "up_id":
                    address = self.genAddress(values[0][n])
                    infos["address"] = address
                n += 1
            
            if type == "files":
                if infos["type"] != "other":
                    self.query.setStatTrue("pragma")
                    self.query.setTables([typeDb[infos["type"]]])
                    keys = DB.execute(self.query.returnQuery())
                    
                    self.query.setStatTrue("select")
                    self.query.setSelect(["*"])
                    self.query.setTables([typeDb[infos["type"]]])
                    self.query.setWhere([{"f_id":id}])
                    values = DB.execute(self.query.returnQuery())
                    
                    n = 0
                    while n<len(keys):
                        if keys[n][1] != "f_id":
                            infos[keys[n][1]] = values[0][n]
                        n += 1
                        
            text = ""
            if len(infos.keys())>0:
                for i in KeysQuene:
                    if infos.has_key(i):
                        if infos[i] == "" or infos[i] == 0:
                            pass
                        else:
                            text += "%20s : %s\n"% (TransKeys[i], infos[i])
            return text
        



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
