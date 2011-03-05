#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database
import datetime

from warnings import simplefilter # for ignoriny DeprecationWarning.
simplefilter("ignore", DeprecationWarning)

#eksik bağımlılıkların belirlenmesi ve modüllerin çağrılması
try:
    import kaa.metadata as Meta
    EnableMetaData = True
except:
    EnableMetaData = False

try:
    import pyPdf
    EnablePdf = True
except:
    EnablePdf = False

try:
    from mutagen.mp3 import MP3
    from mutagen.easyid3 import EasyID3
    EnableMp3 = True
except:
    EnableMp3 = False

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

DB = database.dataBase()
Query = database.EditQuery()

class Item(object):
    """Sistemdeki gerçek dosyaları/dizinleri belirtmek için oluşturulan nesne"""
    attributes = ["up_id","name","type","size","description","datecreate",
                  "datemodify","dateaccess","dateinsert"]
    def __init__(self, form, info):
        """Nesnenin tanımlanması için fonksiyon.
        
        form -> "file" or "directory"
        info -> dict {key:value} -> keys in self.attributes
        """
        self.form = form
        for i in self.attributes:
            if i in info.keys():
                setattr(self, i, info[i])
            else:
                if i in ["datecreate","datemodify","dateaccess","dateinsert"]:
                    setattr(self, i, datetime.datetime.now())
                elif self.form == "file":
                    if i == "size":
                        setattr(self, i, 0)
                    elif i == "type":
                        setattr(self, i, "other")
                elif self.form == "directory":
                    if i == "description":
                        setattr(self, i, "")
        
    def setAddress(self, address):
        """Dosya/dizin bilgilerini verilen adresteki dosyadan/dizinden elde
        eden fonksiyon.
        
        setAddress(address)
        address -> "/address/line"
        """
        if address[-1] == os.sep:
            address = address[:-1]
        setattr(self, "address", address)
        
        status = os.stat(address)
        setattr(self, "datecreate",
                datetime.datetime.fromtimestamp(status.st_ctime))
        setattr(self, "datemodify",
                datetime.datetime.fromtimestamp(status.st_mtime))
        setattr(self, "dateaccess",
                datetime.datetime.fromtimestamp(status.st_atime))
        setattr(self, "dateinsert",
                datetime.datetime.now())
        if os.path.isfile(address):
            setattr(self, "size", int(status.st_size))
            
        if "name" not in dir(self) or getattr(self, "name") == "":
            name = os.path.split(address)[-1]
            setattr(self, "name", name)
            
    def getinfo(self):
        """Nesne, elde ettiği bilgileri sözlük olarak döner.
        
        getinfo() -> {key:value} -> key in self.attributes
        """
        info = {}
        for i in self.attributes:
            if i in dir(self):
                info[i] = getattr(self, i)
        if info.has_key("name") and info.has_key("up_id"):
            return info
        else:
            return False
        
class DetailItem(object):
    """Dosyalar için ayrıntılı bilgi elde etmek için oluşturulan nesne."""
    fileType = {"ebook":[".pdf"],
                "image":[".bmp",".jpeg",".jpg",".png"],
                "music":[".aac",".acc",".mp3",".ogg",".wma"],
                "video":[".avi",".flv",".mp4",".mpeg",".mpg"]}
    def __init__(self, name, address=None, info=None, book=False):
        """Ayrıntılı bilgi nesnesinin tanımlanması için fonksiyon.
        
        name -> str
        address -> None or "/address/line"
        info -> None or dict {key:value}
        book -> False or True
        """
        for i in self.fileType.keys():
            self.ext = os.path.splitext(name)[-1]
            if self.ext in self.fileType[i]:
                self.kind = i
                break
                
        if book:
            self.kind = "book"
            self.info = info
            
        self.address = address
        self.realinfo = info
            
        if "kind" not in dir(self):
            self.kind = "other"
                
    def getInfos(self):
        """Ayrıntılı bilgileri elde edecek fonksiyon. Dosya ayrıntılı bilgiyi
        destekliyorsa True, desteklemiyorsa False döner.
        
        getInfos() -> True or False
        """
        self.info = {}
        if self.kind == "book":
            self.info = self.bookInfo()
        elif self.kind == "image" and EnableMetaData:
            self.info = imageInfo(self.address)
        elif self.kind == "video" and EnableMetaData:
            self.info = self.videoInfo()
        elif self.kind == "ebook" and EnablePdf:
            self.info = self.ebookInfo()
        elif self.ext == ".mp3" and EnableMp3:
            self.info = self.mp3Tags()
        elif self.kind == "music" and EnableMetaData:
            self.info = self.musicInfo()
        else:
            return False
        return True
            
    def bookInfo(self):
        """Kitaplar için ayrıntıların ayarlanması"""
        info = {"author":"","imprintinfo":"","callnumber":"","page":0,"year":0}
        for i in info.keys():
            if i in self.realinfo.keys():
                info[i] = realinfo[i]
        return info
                
    def imageInfo(self):
        """Resimler için ayrıntıların ayarlanması"""
        info = {"width":0,"height":0}
        if self.address:
            realinfo = Meta.parse(self.address)
        elif self.realinfo:
            realinfo = self.realinfo
        for i in info.keys():
            if realinfo.has_key(i) and realinfo[i] != None:
                info[i] = realinfo[i]
        return info
        
    def videoInfo(self):
        """Videolar için ayrıntıların ayarlanması"""
        info = {"title":"","length":0,"width":0,"height":0}
        if self.address:
            realinfo = Meta.parse(self.address)
        elif self.realinfo:
            realinfo = self.realinfo
        for i in info.keys():
            if realinfo.has_key(i) and realinfo[i] != None:
                info[i] = realinfo[i]
        return info
        
    def ebookInfo(self):
        """Elektronik kitaplar için ayrıntıların ayarlanması"""
        info = {"author":"","title":"","year":0,"page":0}
        if self.address:
            openPdf = open(self.address, "r")
            pdfFile = pyPdf.PdfFileReader(openPdf)
            pdfInfos = pdfFile.getDocumentInfo()
            if pdfInfos.has_key("/Author"):
                info["author"] = pdfInfos["/Author"]
            if pdfInfos.has_key("/Title"):
                info["title"] = pdfInfos["/Title"]
            if pdfInfos.has_key("/CreationDate"):
                info["year"] = int(pdfInfos["/CreationDate"][2:6])
            info["page"] = int(pdfFile.getNumPages())
        elif self.realinfo:
            realinfo = self.realinfo
            for i in info.keys():
                if realinfo.has_key(i):
                    info[i] = realinfo[i]
        return info
        
    def mp3Tags(self):
        """MP3'ler için ayrıntıların ayarlanması"""
        info = {"title":"","artist":"","album":"","date":0,"tracknumber":0,
                "genre":"","bitrate":0,"samplerate":0,"length":0}
        if self.address:
            realinfo = MP3(self.address, EasyID3)
            info["bitrate"] = realinfo.info.bitrate
            info["samplerate"] = realinfo.info.sample_rate
            info["length"] = int(float(realinfo.info.length))
            for i in info.keys():
                if realinfo.has_key(i):
                    info[i] = realinfo[i][0]
        elif self.realinfo:
            realinfo = self.realinfo
            for i in info.keys():
                if realinfo.has_key(i):
                    info[i] = realinfo[i]
        return info
        
    def musicInfo(self):
        """Müzikler için ayrıntıların ayarlanması"""
        turnKeys = {"date":"userdate","tracknumber":"trackno"}
        info = {"title":"","artist":"","album":"","date":0,"tracknumber":0,
                "genre":"","bitrate":0,"samplerate":0,"length":0}
        if self.address:
            realinfo = Meta.parse(self.address)
            for i in info.keys():
                if i in turnKeys.keys() and realinfo[turnKeys[i]] != None:
                    info[i] = int(realinfo[turnKeys[i]])
                elif realinfo[i] != None:
                    if i == "bitrate":
                        info[i] = realinfo[i]*1000
                    elif i == "length":
                        info[i] = int(realinfo[i])
                    else:
                        info[i] = realinfo[i]
        elif self.realinfo:
            realinfo = self.realinfo
            for i in info.keys():
                if realinfo.has_key(i):
                    info[i] = realinfo[i]
        return info
        
def createDir(item):
    """Veritabanına dizin eklemek için oluşturulan fonksiyon.
    
    createDir(Item)
    """
    if item.form == "directory":
        info = item.getinfo()
        if info:
            keys = info.keys()
            values = []
            for i in keys:
                values.append(info[i])
                
            Query.setStatTrue("insert")
            Query.setTables(["dirs"])
            Query.setKeys(keys)
            Query.setValues(values)
            DB.execute(Query.returnQuery())
            
            Query.setStatTrue("select")
            Query.setSelect(["max(id)"])
            Query.setTables(["dirs"])
            up = DB.execute(Query.returnQuery())[0][0]
            
            if "address" in dir(item):
                for i in os.listdir(item.address):
                    address = item.address + os.sep + i
                    
                    if os.path.isdir(address):
                        tempItem = Item(form="directory", info={"up_id":up})
                        tempItem.setAddress(address)
                        
                        createDir(tempItem)
                        
                    elif os.path.isfile(address):
                        tempItem = Item(form="file", info={"up_id":up})
                        tempItem.setAddress(address)
                        
                        detItem = DetailItem(name=i, address=address)
                        if detItem.getInfos():
                            createFile(tempItem, detItem)
                        else:
                            createFile(tempItem)
    
def createFile(item, detailItem=None):
    """Veritabanına dosya eklemek için oluşturulan fonksiyon.
    
    createFile(Item, DetailItem=None)
    """
    if item.form == "file":
        info = item.getinfo()
        if info:
            keys = info.keys()
            values = []
            for i in keys:
                values.append(info[i])
                
            Query.setStatTrue("insert")
            Query.setTables(["files"])
            Query.setKeys(keys)
            Query.setValues(values)
            DB.execute(Query.returnQuery())
            
            Query.setStatTrue("select")
            Query.setSelect(["max(id)"])
            Query.setTables(["files"])
            fId = DB.execute(Query.returnQuery())[0][0]
            
            if detailItem:
                kind = detailItem.kind
                kindTable = kind[0] + "info"
                detInfo = detailItem.info
                
                detInfo["f_id"] = fId
                
                keys, values = detInfo.keys(), []
                for i in keys:
                    values.append(detInfo[i])
                
                Query.setStatTrue("insert")
                Query.setTables([kindTable])
                Query.setKeys(keys)
                Query.setValues(values)
                DB.execute(Query.returnQuery())
                
