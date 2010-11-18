#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import datetime
import database
import detailer

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

DB = database.dataBase()
Query = database.EditQuery()

class Item(object):
    """Bilge-katalog'da dosya ve dizinlerin bilgilerini tutmak için nesne.
    
    Değişkenler:
    no -- int
    name -- str
    form -- "file" or "directory"
    address -- str "/foo/bar"
    updirs -- list [firstUp(Item), secondUp(Item),...]
    """
    no = None
    name = None
    form = None
    address = None
    updirs = None
    
    def setItem(self, no, name, form):
        """nesne(item) için no, name ve form değişkenlerini ayarlama
        
        setItem(no, name, form)
        
        Keyword arguments:
        no -- int
        name -- str
        form -- "file" or "directory"
        """
        self.no = no
        self.name = name
        self.form = form
        self.setAddress()
        
    def setAddress(self):
        """\
        Nesne(item) için adres bilgisini ve üst dizinler listesini doldurur.\
        """
        self.address = "/"
        self.updirs = []
        tempNames = []
        no = self.no
        form = self.form
        while no != 0:
            Query.setStatTrue("select")
            Query.setSelect(["id", "up_id", "name"])
            if form == "directory":
                Query.setTables(["dirs"])
            elif form == "file":
                Query.setTables(["files"])
            Query.setWhere([{"id":no}])
            noid, no, name = DB.execute(Query.returnQuery())[0]
            form = "directory"
            if noid != self.no:
                tempItem = Item()
                tempItem.setItem(noid, name, "directory")
                self.updirs.append(tempItem)
            tempNames.append(name)
        tempNames.reverse()
        for i in tempNames:
            self.address += i
            if i != self.name or self.form == "directory":
                self.address += "/"
    
class RootItem(Item):
    """Kök dizini belirtmek için oluşturulmuş özel nesne"""
    def __init__(self):
        self.no = 0
        self.name = "ROOT"
        self.form = "directory"
        self.address = "/"
        self.updirs = []
    
class Explore(object):
    """Bilge-Katalog için dizinlerde gezinme sınıfı."""
    def __init__(self):
        """Gezinme sınıfı için kök dizini ve içeriğinin listesinin
        hazırlanması."""
        self.curItem = RootItem()
        self.curItemList = self.fillList()
        
    def fillList(self, item=None):
        """Dizin içeriğindeki nesneleri dönen fonksiyondur.
        
        fillList(Item) -> [Item1, Item2,...]
        
        fillList() = fillList(Şuanki dizin nesnesi)
        """
        itemList = []
        if item:
            dirNo = item.no
        else:
            dirNo = self.curItem.no
        
        Query.setStatTrue("select")
        Query.setSelect(["id", "name"])
        Query.setTables(["dirs"])
        Query.setWhere([{"up_id":dirNo}])
        for i in DB.execute(Query.returnQuery()):
            tempItem = Item()
            tempItem.setItem(no=i[0], name=i[1], form="directory")
            itemList.append(tempItem)
           
        Query.setStatTrue("select")
        Query.setSelect(["id", "name"]) 
        Query.setTables(["files"])
        Query.setWhere([{"up_id":dirNo}])
        for i in DB.execute(Query.returnQuery()):
            tempItem = Item()
            tempItem.setItem(no=i[0], name=i[1], form="file")
            itemList.append(tempItem)
            
        return itemList
        
    def ls(self, item=None):
        """Dizin içeriğindeki nesnelerin adlarını yazdıran fonksiyon.
        
        ls(Item) -> print "     Name : NAME
                                 key : values       "
        
        ls() = ls(Şuanki dizin nesnesi)
        """
        if item:
            listOfItems = self.fillList(item)
        else:
            listOfItems = self.curItemList
            
        if len(listOfItems) > 0:
            for i in listOfItems:
                print i.name
        
    def chdir(self, item):
        """Bulunulan dizindeki bir dizine girmek için kullanılır.
        
        chdir(Item)
        """
        dirName = item.name
        tempName = ""
        tempIndex = 0
        while not dirName == tempName:
            tempName = self.curItemList[tempIndex].name
            if dirName == tempName:
                self.curItem = self.curItemList[tempIndex]
            tempIndex += 1
        self.curItemList = self.fillList()
        
    def turnUp(self):
        """Üst dizine çıkmak için kullanılır."""
        if len(self.curItem.updirs) > 0:
            self.curItem = self.curItem.updirs[0]
            self.curItemList = self.fillList()
        elif len(self.curItem.updirs) == 0:
            self.curItem = RootItem()
            self.curItemList = self.fillList()
        
class UseItem(object):
    """Dosya/Dizin işlemleri için oluşturulan sınıftır."""
    pass
    
class User(object):
    """Bilge-Katalog için kullanıcı nesnesi
    
    Değişkenler:
    id -- int
    name -- str
    surname -- str
    email -- str
    mobile -- str
    home -- str
    work -- str
    address --str
    """
    def __init__(self):
        """Kullanıcı nesnesi için özelliklerin ayarlanması"""
        self.attributes = ["id", "name", "surname", "email", "mobile", "home",
                           "work", "address"]
        for i in self.attributes:
            setattr(self, i, None)
    def dictTypeInfo(self):
        """Kullanıcı bilgilerini sözlük olarak döner.
        
        dictTypeInfo() -> {"id":"ID","name":"NAME","surname":"SURNAME",...}
        """
        infos = {}
        for i in self.attributes:
            if getattr(self, i):
                infos[i] = getattr(self, i)
        return infos
    def textTypeInfo(self):
        """Kullanıcı bilgilerini yazı olarak döner.
        
        textTypeInfo() -> "      Id : ID
                               Name : NAME
                            Surname : SURNAME   "
        """
        text = ""
        for i in self.attributes:
            if getattr(self, i):
                text += "%20s : %s\n"% (i, getattr(self, i))
        return text
        
class Users(object):
    """Bilge-Katalog için kullanıcıların yönetimi."""
    def add(self, user):
        """Yeni kullanıcı ekler.
        
        add(User)
        """
        infos = user.dictTypeInfo()
        keys, values = [], []
        for i in infos.keys():
            keys.append(i)
            values.append(infos[i])
        
        Query.setStatTrue("insert")
        Query.setTables(["users"])
        Query.setKeys(keys)
        Query.setValues(values)
        
        DB.execute(Query.returnQuery())
        
    def info(self, no):
        """Kullanıcı id'sinden kullanıcı bilgileri ile kullanıcı nesnesi
        döner.
        
        info(int) -> User
        """
        Query.setStatTrue("pragma")
        Query.setTables(["users"])
        keys = DB.execute(Query.returnQuery())
        
        Query.setStatTrue("select")
        Query.setSelect(["*"])
        Query.setTables(["users"])
        Query.setWhere([{"id":no}])
        values = DB.execute(Query.returnQuery())[0]
        
        user = User()
        n = 0
        while len(keys) > n:
            setattr(user, keys[n][1], values[n])
            n += 1
            
        return user
        
    def update(self, user):
        """Kullanıcı bilgilerini günceller.
        
        update(User)
        """
        infos = user.dictTypeInfo()
        no = infos["id"]
        del infos["id"]
        if len(infos.keys())>0:
            Query.setStatTrue("update")
            Query.setTables(["users"])
            Query.setSet(infos)
            Query.setWhere([{"id":no}])
            
            DB.execute(Query.returnQuery())
            
class Tags(object):
    pass
    
class LendItem(object):
    pass
