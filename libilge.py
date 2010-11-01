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

TransKeys = {   "id"            :   _("Identify"),
                "name"          :   _("Name"),
                "surname"       :   _("Surname"),
                "email"         :   _("E-mail"),
                "mobile"        :   _("Mobile Number"),
                "home"          :   _("Home Number"),
                "work"          :   _("Work Number"),
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
                "height"        :   _("Height"),
                "tags"          :   _("Tags")    }

KeysQuene = [   "id", "name", "surname", "email", "mobile", "home", "work", 
                "address", "size", "type", "description", "title",
                "artist", "album", "date", "tracknumber", "genre", "bitrate",
                "samplerate", "length", "author", "page", "year",
                "callnumber", "imprintinfo", "width", "height", "datecreate",
                "datemodify", "dateaccess", "dateinsert", "tags"]

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
    elif type == ".pdf":
        infos = detailer.pdfInfo(address)
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
        
        if address and infos["up_id"] != 0:
            if not infos.has_key("name"):
                infos["name"] = os.path.split(address)[-1]
                if infos["name"] == "":
                    infos["name"]=os.path.split(os.path.split(address)[0])[-1]
            
            stat = os.stat(address)
            infos["datecreate"] = datetime.datetime.fromtimestamp(stat.st_ctime)
            infos["datemodify"] = datetime.datetime.fromtimestamp(stat.st_mtime)
            infos["dateaccess"] = datetime.datetime.fromtimestamp(stat.st_atime)
            infos["dateinsert"] = datei
        
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
        
        if infos.has_key("tags"):
            tags = infos["tags"]
            self.addTags(id=upId, type="directory", tags=tags)
        
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
                    
    def mkFile(self, address=None, infos={}, details=None):
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
        
        if not infos.has_key("up_id"):
            infos["up_id"] = self.dirNow
            
        name = infos["name"]
        if types.has_key(name[-4:].lower()) and infos.has_key("type") == False:
            infos["type"] = types[name[-4:].lower()]
            if address:
                details = tagging(address, name[-4:].lower())
        elif infos.has_key("type") == False:
            infos["type"] = "other"
            
        if not infos.has_key("datecreate"):
            infos["datecreate"] = datetime.datetime.now()
            infos["datemodify"] = datetime.datetime.now()
            infos["dateaccess"] = datetime.datetime.now()
            infos["dateinsert"] = datetime.datetime.now()
        
        if not infos.has_key("size"):
            infos["size"] = 0
        
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
        
        if infos.has_key("tags"):
            tags = infos["tags"]
            self.query.setStatTrue("select")
            self.query.setSelect(["max(id)"])
            self.query.setTables(["files"])
            fId = DB.execute(self.query.returnQuery())[0][0]
            self.addTags(id=fId, type="file", tags=tags)
        
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
        
        
    def dirList(self, id=None, dirname=None, partite=False):
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
                self.dirList(id=dirs[dirname], partite=partite)
            except KeyError:
                print _("%s is not a directory"% dirname)
        
        elif partite:
            return dirs, files
            
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
            elif dirname != "":
                dirs = {}
                self.query.setStatTrue("select")
                self.query.setSelect(["id", "name"])
                self.query.setTables(["dirs"])
                self.query.setWhere([{"up_id":self.dirNow}])
                Dirs = DB.execute(self.query.returnQuery())
                for i in Dirs:
                    dirs[i[1]]=i[0]                    
                if dirs.has_key(dirname):
                    self.dirNow = dirs[dirname]
                else:
                    return False
            return True
                        
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
        
        self.editTags(id, "directory", "") #delete tags
        
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
                id, type = files[filename]
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
            
            self.editTags(id, "file", "") # delete tags
            
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
        
    def parseAddress(self, address):
        addressList = []
        if "/" in address:
            if address.find("/") == 0:
                addressList.append("/")
            parts = address.split("/")
            for i in parts:
                if i != "":
                    addressList.append(i)
        else:
            addressList.append(address)
        return addressList
        
    def info(self, id=None, name=None, type=None, redict=False):
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
                infos["tags"] = self.getTags(id, "file")
            elif type == "dirs":
                infos["tags"] = self.getTags(id, "directory")
            
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
                    
                    if values != []:
                        n = 0
                        while n<len(keys):
                            if keys[n][1] != "f_id":
                                infos[keys[n][1]] = values[0][n]
                            n += 1
                        
            text = ""
            if len(infos.keys())>0:
                if redict:
                    return infos
                else:
                    for i in KeysQuene:
                        if infos.has_key(i):
                            if infos[i] == "" or infos[i] == 0:
                                pass
                            else:
                                text += "%20s : %s\n"% (TransKeys[i], infos[i])
            return text
        
    def search(self, wanted="", detail=""):
        if wanted:
            dirs, files = [], []
            self.query.setStatTrue("select")
            self.query.setSelect(["id","name","up_id"])
            self.query.setTables(["files"])
            self.query.setWhereLike([{"name":wanted}])
            FilesReq = DB.execute(self.query.returnQuery())
            for i in FilesReq:
                address = self.genAddress(i[2])
                files += [(i[0], i[1], address, "files")]
                
            self.query.setSelect(["id","name","up_id"])
            self.query.setTables(["dirs"])
            self.query.setWhereLike([{"name":wanted}, "OR",
                                     {"description":wanted}])
            DirsReq = DB.execute(self.query.returnQuery())
            for i in DirsReq:
                address = self.genAddress(i[2])
                dirs += [(i[0], i[1], address, "dirs")]
                
            wantedList = dirs + files
            
            if detail == "basic":
                return wantedList
            elif detail == "all":
                textList = [wanted + ":"]
                for i in wantedList:
                    text = self.info(id=i[0], type=i[3])
                    textList.append(i[1] + "\n" + text)
                return textList
            elif detail == "address":
                addresses = [wanted + ":"]
                for i in wantedList:
                    addresses.append(" " + i[2] + i[1])
                return addresses

    def update(self, updated, parameters):
        dirs, files = {}, {}
        self.query.setStatTrue("select")
        self.query.setSelect(["id", "name"])
        self.query.setTables(["dirs"])
        self.query.setWhere([{"up_id":self.dirNow}])
        Dirs = DB.execute(self.query.returnQuery())
        for i in Dirs:
            dirs[i[1]]=str(i[0])
        self.query.setSelect(["id", "name", "type"])
        self.query.setTables(["files"])
        Files = DB.execute(self.query.returnQuery())
        for i in Files:
            files[i[1]]=str(i[0])
            type = i[2]
        if files.has_key(updated):
            table = "files"
            ids = files[updated]
            if parameters.has_key("tags"):
                self.editTags(ids, "file", parameters["tags"])
        elif dirs.has_key(updated):
            table = "dirs"
            ids = dirs[updated]
            if parameters.has_key("tags"):
                self.editTags(ids, "directory", parameters["tags"])
        else:
            return False
        
        usingParams = {}
        keys = []
        self.query.setStatTrue("pragma")
        if table == "files":
            self.query.setTables(["files"])
            Keys = DB.execute(self.query.returnQuery())
            for i in Keys:
                keys.append(i[1])
            if type != "other":
                self.query.setTables([typeDb[type]])
                Keys = DB.execute(self.query.returnQuery())
                for i in Keys:
                    keys.append(i[1])
        elif table == "dirs":
            self.query.setTables(["dirs"])
            Keys = DB.execute(self.query.returnQuery())
            for i in Keys:
                keys.append(i[1])
                
        for i in keys:
            if parameters.has_key(i):
                usingParams[i] = parameters[i]
        
        if table == "files":
            try:
                numb = keys.index("f_id")
                inf = keys[:numb]
                det = keys[numb:]
            except ValueError:
                inf = []
                for i in keys:
                    inf.append(i)
                det = []
            
            info = {}
            detail = {}
            
            for i in usingParams.keys():
                if i in inf:
                    info[i] = usingParams[i]
                if i in det:
                    detail[i] = usingParams[i]
                    
            if len(info.keys())>0:
                self.query.setStatTrue("update")
                self.query.setTables(["files"])
                self.query.setSet(info)
                self.query.setWhere([{"id":ids}])
                DB.execute(self.query.returnQuery())
                
            if type != "other":
                update = False
                self.query.setStatTrue("select")
                self.query.setTables([typeDb[type]])
                self.query.setSelect(["*"])
                self.query.setWhere([{"f_id":ids}])
                if DB.execute(self.query.returnQuery()) != []:
                    update = True
                if len(detail.keys())>0 and type != "other" and update:
                    self.query.setStatTrue("update")
                    self.query.setTables([typeDb[type]])
                    self.query.setSet(detail)
                    self.query.setWhere([{"f_id":ids}])
                    DB.execute(self.query.returnQuery())
                elif len(detail.keys())>0 and type != "other" and update == False:
                    infoDet = detailer.getKeys(typeDb[type])
                    infoDet["f_id"]=ids
                    for i in detail.keys():
                        infoDet[i] = detail[i]
                    
                    keys, values = [], []
                    for i in infoDet.keys():
                        keys.append(i)
                        values.append(infoDet[i])
                    self.query.setStatTrue("insert")
                    self.query.setTables([typeDb[type]])
                    self.query.setKeys(keys)
                    self.query.setValues(values)
                    DB.execute(self.query.returnQuery())
                    
        elif table == "dirs":
            if len(usingParams.keys())>0:
                self.query.setStatTrue("update")
                self.query.setTables(["dirs"])
                self.query.setSet(usingParams)
                self.query.setWhere([{"id":ids}])
                DB.execute(self.query.returnQuery())
    
    
    def copy(self, name=None, to=[]):
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
        
            if type == "files":
                self.copyFile(id=id, to=to)
            elif type == "dirs":
                self.copyDir(id=id, to=to)
        
    def copyFile(self, id=None, to=[]):
        infos, details = {}, {}
        oldId = self.dirNow
        for i in to[:-1]:
            if i:
                stat = self.chDir(dirname=i)
                if stat != True:
                    print _("%s is not a directory"% i)
        stat = self.chDir(dirname=to[-1])
        if stat != True:
            infos["name"] = to[-1]
        infos["up_id"] = self.dirNow
        self.dirNow = oldId
        
        infosOrj = self.info(id=id, type="files", redict=True)
        
        for i in infosOrj.keys():
            if i in ["size", "type", "datecreate", "datemodify", "dateaccess",
                     "dateinsert"]:
                infos[i] = infosOrj[i]
            elif not infos.has_key("name") and i == "name":
                infos[i] = infosOrj[i]
            elif not i in ["up_id", "address"]:
                details[i] = infosOrj[i]
                
        self.mkFile(infos=infos, details=details)
        
    def copyDir(self, id=None, to=[]):
        infos = {}
        oldId = self.dirNow
        for i in to[:-1]:
            if i:
                stat = self.chDir(dirname=i)
                if stat != True:
                    print _("%s is not a directory"% i)
        stat = self.chDir(dirname=to[-1])
        if stat != True:
            infos["name"] = to[-1]
        infos["up_id"] = self.dirNow
        self.dirNow = oldId
        
        infosOrj = self.info(id=id, type="dirs", redict=True)
        
        for i in infosOrj.keys():
            if i in ["description", "datecreate", "datemodify", "dateaccess",
                     "dateinsert"]:
                infos[i] = infosOrj[i]
            elif not infos.has_key("name") and i == "name":
                infos[i] = infosOrj[i]
                
        self.mkDir(infos=infos)
        
        if to[-1] != infos["name"]:
            to.append(infos["name"])
        
        dirs, files = self.dirList(id=id, partite=True)
        
        for i in files.keys():
            self.copyFile(id=files[i], to=to)
            
        for i in dirs.keys():
            self.copyDir(id=dirs[i], to=to)
        
    def addTags(self, id, type, tags):
        tagsList = tags.split(",")
        try:
            tagsList.remove("")
        except ValueError:
            pass
        for tag in tagsList:
            try:
                self.query.setStatTrue("select")
                self.query.setSelect(["id"])
                self.query.setTables(["tags"])
                self.query.setWhereLike([{"name":tag.strip()}])
                tagId = DB.execute(self.query.returnQuery())[0][0]
            except IndexError:
                self.query.setStatTrue("insert")
                self.query.setTables(["tags"])
                self.query.setKeys(["name"])
                self.query.setValues([tag.strip()])
                DB.execute(self.query.returnQuery())
                
                self.query.setStatTrue("select")
                self.query.setSelect(["max(id)"])
                self.query.setTables(["tags"])
                tagId = DB.execute(self.query.returnQuery())[0][0]
            if type == "directory":
                self.query.setStatTrue("insert")
                self.query.setTables(["tagdirs"])
                self.query.setKeys(["d_id", "tags_id"])
                self.query.setValues([id, tagId])
                DB.execute(self.query.returnQuery())
            if type == "file":
                self.query.setStatTrue("insert")
                self.query.setTables(["tagfiles"])
                self.query.setKeys(["f_id", "tags_id"])
                self.query.setValues([id, tagId])
                DB.execute(self.query.returnQuery())
        
    def getTags(self, id, type):
        tags = ""
        self.query.setStatTrue("select")
        self.query.setSelect(["tags.name"])
        if type == "file":
            self.query.setTables(["tags","tagfiles"])
            self.query.setWhere([{"tags.id":"tagfiles.tags_id"},
                                  "AND", {"tagfiles.f_id":id}])
        elif type == "directory":
            self.query.setTables(["tags","tagdirs"])
            self.query.setWhere([{"tags.id":"tagdirs.tags_id"},
                                  "AND", {"tagdirs.d_id":id}])
        for i in DB.execute(self.query.returnQuery()):
            tags += i[0] + ","
            
        if len(tags)>0:
            return tags
        else:
            return ""
                
    def editTags(self, id, type, tags):
        oldTags, newTags = set(), set()
        for i in tags.split(","):
            if not i == "":
                newTags.add(i)
            
        for i in self.getTags(id, type).split(","):
            if not i == "":
                oldTags.add(i)
                
        delTags = oldTags - newTags
        addTags = ""
        for i in (newTags - oldTags):
            if  not i == "":
                addTags += i + ","
        
        for i in delTags:
            self.query.setStatTrue("select")
            self.query.setSelect(["tags.id"])
            self.query.setTables(["tags"])
            self.query.setWhere([{"tags.name":"'%s'"% i}])
            tagId = self.query.returnQuery()[0]
            
            self.query.setStatTrue("delete")
            if type == "file":
                self.query.setTables(["tagfiles"])
                self.query.setWhere([{"(%s)"% tagId:"tagfiles.tags_id"},
                                      "AND", {"tagfiles.f_id":id}])
            elif type == "directory":
                self.query.setTables(["tagdirs"])
                self.query.setWhere([{"(%s)"% tagId:"tagdirs.tags_id"},
                                      "AND", {"tagdirs.d_id":id}])
            if type:
                DB.execute(self.query.returnQuery())
            
        if len(addTags)>0:
            self.addTags(id, type, addTags)
            
    def lend(self, lended, uid=None):
        isReserve = False
        now = datetime.datetime.now()
        status = "lended"
        extension = 0
        kind = None
        dirs, files = self.dirList(partite=True)
        if lended in dirs.keys():
            kind = "dirs"
            k_id = dirs[lended]
        if lended in files.keys():
            kind = "files"
            k_id = files[lended]
        
        if kind != None:
            self.query.setStatTrue("select")
            self.query.setTables(["lend"])
            self.query.setSelect(["*"])
            self.query.setWhere([{"kind":"'%s'"% kind}, "AND", {"k_id":k_id},
                                 "AND", {"status":"'lended'"}])
            request = DB.execute(self.query.returnQuery())
            if len(request)>0:
                return (False, _("That object is lended."))
            else:
                reserveList = self.getReserveList(lended)
                if uid == None:
                    if len(reserveList)>0:
                        uid = reserveList[0]
                        isReserve = True
                    else:
                        return (False, _("No user id given!"))
                        
                if len(reserveList)>0 and uid == reserveList[0]:
                    isReserve = True
                    
                if len(reserveList)>0 and uid != reserveList[0]:
                    return (False, _("Wait for the order!"))
                    
                else:
                    self.query.setStatTrue("select")
                    self.query.setSelect(["*"])
                    self.query.setTables(["users"])
                    self.query.setWhere([{"id":uid}])
                    request2 = DB.execute(self.query.returnQuery())
                    if not len(request2)>0:
                        return (False, _("That user not registered!"))
                    
                    if isReserve:
                        self.query.setStatTrue("update")
                        self.query.setTables(["lend"])
                        self.query.setSet({"lenddate":now,
                                            "extension":extension,
                                            "status":status})
                        self.query.setWhere([{"kind":"'%s'"% kind}, "AND",
                                             {"k_id":k_id}, "AND",
                                             {"status":"'waiting'"}, "AND",
                                             {"u_id":uid}])
                        DB.execute(self.query.returnQuery())
                    else:
                        self.query.setStatTrue("insert")
                        self.query.setTables(["lend"])
                        self.query.setKeys(["kind", "k_id", "u_id",
                                            "lenddate", "extension",
                                            "status"])
                        self.query.setValues([kind, k_id, uid, now, extension,
                                              status])
                        DB.execute(self.query.returnQuery())
                    
                    self.query.setStatTrue("select")
                    self.query.setTables(["lend"])
                    self.query.setSelect(["id"])
                    self.query.setWhere([{"kind":"'%s'"% kind}, "AND",
                                         {"k_id":k_id}, "AND",
                                         {"status":"'lended'"}, "AND",
                                         {"u_id":uid}])
                    bid = DB.execute(self.query.returnQuery())[0][0]
                    
                    text = ""
                    text += "%20s : %s\n"% (_("Lending ID"), bid)
                    text += "%20s : %s\n"% (_("Lended"), lended)
                    text += "%20s : %s\n"% (_("Borrower ID"), uid)
                    
                    return (True, text)
        
    def takeback(self, lended):
        status = "returned"
        dirs, files = self.dirList(partite=True)
        if lended in dirs.keys():
            kind = "dirs"
            k_id = dirs[lended]
        if lended in files.keys():
            kind = "files"
            k_id = files[lended]
            
        self.query.setStatTrue("update")
        self.query.setSet({"status":status})
        self.query.setTables(["lend"])
        self.query.setWhere([{"kind":"'%s'"% kind}, "AND", {"k_id":k_id},
                             "AND", {"status":"'lended'"}])
                             
        DB.execute(self.query.returnQuery())
        
    def getReserveList(self, lended):
        dirs, files = self.dirList(partite=True)
        if lended in dirs.keys():
            kind = "dirs"
            k_id = dirs[lended]
        if lended in files.keys():
            kind = "files"
            k_id = files[lended]
            
        reserveList = []
        
        self.query.setStatTrue("select")
        self.query.setSelect(["u_id"])
        self.query.setTables(["lend"])
        self.query.setWhere([{"kind":"'%s'"% kind}, "AND", {"k_id":k_id},
                             "AND", {"status":"'waiting'"}])
        request = DB.execute(self.query.returnQuery())        
        for i in request:
            reserveList.append(i[0])
            
        return reserveList
        
    def reserve(self, reserved, uid):
        status = "waiting"
        kind = None
        dirs, files = self.dirList(partite=True)
        if reserved in dirs.keys():
            kind = "dirs"
            k_id = dirs[reserved]
        if reserved in files.keys():
            kind = "files"
            k_id = files[reserved]
            
        self.query.setStatTrue("insert")
        self.query.setTables(["lend"])
        self.query.setKeys(["kind", "k_id", "u_id", "status"])
        self.query.setValues([kind, k_id, uid, status])
        DB.execute(self.query.returnQuery())
        
    def addUser(self, params):
        Keys = detailer.getKeys("users")
        del Keys["id"]
        for i in Keys.keys():
            if params.has_key(i):
                Keys[i] = params[i]
        keys, values = [], []
        for i in Keys.keys():
            keys.append(i)
            values.append(Keys[i])
        
        self.query.setStatTrue("insert")
        self.query.setTables(["users"])
        self.query.setKeys(keys)
        self.query.setValues(values)
        
        DB.execute(self.query.returnQuery())
        
    def delUser(self, id): # kullanıcıda ödünç verilen varsa silmeyi önleme eklenecek
        self.query.setStatTrue("delete")
        self.query.setTables(["users"])
        self.query.setWhere([{"id":id}])
        
        DB.execute(self.query.returnQuery())
        
    def updateUser(self, id, params):
        infos = {}
        Keys = detailer.getKeys("users")
        for i in params.keys():
            if Keys.has_key(i):
                infos[i] = params[i]
            
        if len(infos.keys())>0:
            self.query.setStatTrue("update")
            self.query.setTables(["users"])
            self.query.setSet(infos)
            self.query.setWhere([{"id":id}])
            
            DB.execute(self.query.returnQuery())
        
    def infoUser(self, id, redict=False):
        self.query.setStatTrue("pragma")
        self.query.setTables(["users"])
        keys = DB.execute(self.query.returnQuery())
        
        self.query.setStatTrue("select")
        self.query.setSelect(["*"])
        self.query.setTables(["users"])
        self.query.setWhere([{"id":id}])
        values = DB.execute(self.query.returnQuery())
        
        infos = {}
        n = 0
        while n<len(keys):
            infos[keys[n][1]] = values[0][n]
            n += 1
            
        text = ""    
        if len(infos.keys())>0:
            if redict:
                return infos
            else:
                for i in KeysQuene:
                    if infos.has_key(i):
                        if infos[i] == "" or infos[i] == 0:
                            pass
                        else:
                            text += "%20s : %s\n"% (TransKeys[i], infos[i])
                return text
        
    def searchUserAll(self, searched):
        pass
        
    def searchUserParams(self, params):
        pass
        
