#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import sqlite3

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

DBFile = "database.db"# yerine kullanalım.":memory:"#hız için şimdilik        

class dataBase:
    def __init__(self):
        creating = False
        if not os.path.isfile(DBFile):
            creating = True
        self.db = sqlite3.connect(DBFile, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.db.cursor()
        if creating:
            self.createTables()
            
    def createTables(self):
        self.cur.execute("CREATE TABLE dirs ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "up_id INTEGER, "
               "name TEXT, "
               "datecreate TIMESTAMP, "
               "datemodify TIMESTAMP, "
               "dateaccess TIMESTAMP, "
               "dateaddcat TIMESTAMP, "
               "description TEXT)")
               
        self.cur.execute("CREATE TABLE files ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "up_id INTEGER, "
               "name TEXT, "
               "size INTEGER, "
               "datecreate TIMESTAMP, "
               "datemodify TIMESTAMP, "
               "dateaccess TIMESTAMP, "
               "dateaddcat TIMESTAMP, "
               "type TEXT)")
               
        self.cur.execute("CREATE TABLE minfo ("
               "f_id INTEGER PRIMARY KEY, "
               "title TEXT, "
               "artist TEXT, "
               "album TEXT, "
               "date INTEGER, "
               "tracknumber INTEGER, "
               "genre TEXT, "
               "bitrate INTEGER, "
               "frequence INTEGER, "
               "length INTEGER)")

        self.cur.execute("CREATE TABLE binfo ("
               "f_id INTEGER PRIMARY KEY, "
               "author TEXT, "
               "imprintinfo TEXT, "
               "callnumber TEXT, "
               "year INTEGER, "
               "page INTEGER)")

        self.cur.execute("CREATE TABLE einfo ("
               "f_id INTEGER PRIMARY KEY, "
               "title TEXT, "
               "author TEXT, "
               "year INTEGER, "
               "page INTEGER)")

        self.cur.execute("CREATE TABLE iinfo ("
               "f_id INTEGER PRIMARY KEY, "
               "dimensions TEXT)")

        self.cur.execute("CREATE TABLE vinfo ("
               "f_id INTEGER PRIMARY KEY, "
               "title TEXT, "
               "length INTEGER, "
               "dimensions TEXT)")

        self.cur.execute("CREATE TABLE tags ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "name TEXT)")

        self.cur.execute("CREATE TABLE tagfiles ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "f_id INTEGER, "
               "tags_id INTEGER)")

        self.cur.execute("CREATE TABLE tagdirs ("
               "d_id INTEGER, "
               "tags_id INTEGER)")

        self.cur.execute("CREATE TABLE icons ("
               "f_type TEXT PRIMARY KEY, "
               "icon DATA)")
        
        self.db.commit()
        
        
    def execute(self, query):
        self.cur.execute(query)
        if query.find("SELECT") == 0 or query.find("PRAGMA") == 0:
            return self.cur.fetchall()
        else:
            self.db.commit()
            return True
        
class EditQuery:
    def __init__(self):        
        self.status = { "update" : False,
                        "delete" : False,
                        "insert" : False,
                        "select" : False,
                        "pragma" : False    }
        
        
    def setStatTrue(self, status): # "x"
        for i in self.status.keys():
            if i == status:
                self.status[i] = True
            else:
                self.status[i] = False
            self.query = ""
            self.table = ""
            self.where = ""
            self.set = ""
            self.select = ""
            self.list = ""
            
    def setTables(self, tables): # [x1, x2, ...]
        self.table = ""
        for i in tables:
            self.table += i + ", "
        self.table = self.table[:-2]
        
    def setList(self, lists): # [x1, x2, ...]
        self.list = ""
        for i in lists:
            self.list += i + ", "
        self.list = self.list[:-2]
        
    def setSet(self, setkeys): # {x1:y1, x2:y2, ...}
        self.set = ""
        for i in setkeys.keys():
            self.set += i + "=" + setkeys[i] + ", "
        self.set = self.set[:-2]
        
    def setSelect(self, selections): # [x1, x2, ...]
        self.select = ""
        for i in selections:
            self.select += i + ", "
        self.select = self.select[:-2]
        
    def setWhere(self, where): # [{x1:y1}, op12, {x2:y2}, op23, ...]
        self.where = ""
        for i in where:
            if type(i) == dict:
                self.where += str(i.items()[0][0]) + "=" + str(i.items()[0][1])
            else:
                self.where += " " + i + " "
                
    def setQuery(self):
        self.query = ""
        if self.status["select"]:
            if self.select != "" or self.table != "":
                self.query += "SELECT " + self.select
                self.query += " FROM " + self.table
                if self.where != "":
                    self.query += " WHERE " + self.where
                
        elif self.status["update"]:
            if self.table != "" or self.set != "" or self.where != "":
                self.query += "UPDATE " + self.table
                self.query += " SET " + self.set
                self.query += " WHERE " + self.where
            
        elif self.status["delete"]:
            if self.table != "" or self.where != "":
                self.query += "DELETE FROM " + self.table
                self.query += " WHERE " + self.where
            
        elif self.status["insert"]:
            if self.table != "" or self.list != "":
                self.query += "INSERT INTO " + self.table
                self.query += " VALUES (" + self.list + ")"
            
        elif self.status["pragma"]:
            if self.table != "":
                self.query += "PRAGMA TABLE_INFO(" + self.table + ")"
            
    def returnQuery(self):
        self.setQuery()
        if self.query != "":
            return self.query
        else:
            return False
            
                    
        
        
        
# şimdilik atıl kısım        
        
class other:        
    
    #Adding functions
        
    def addDir(self, up_id, name, datec, datem, datea, datei, desc=''):
        self.cur.execute("INSERT INTO dirs "
                "(up_id, name, datecreate, datemodify, dateaccess, dateaddcat, description) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (up_id, name, datec, datem, datea, datei, desc))
        self.db.commit()
        id = self.cur.execute("SELECT max(id) FROM dirs").fetchone()
        return id[0]
        
    def addFile(self, up_id, name, size, datec, datem, datea, datei, type):
        self.cur.execute("INSERT INTO files "
                "(up_id, name, size, datecreate, datemodify, dateaccess, dateaddcat, type) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (up_id, name, size, datec, datem, datea, datei, type))
        self.db.commit()
        id = self.cur.execute("SELECT max(id) FROM files").fetchone()
        return id[0]
        
    def addBook(self, f_id, author, imprintinfo, callnumber, year, page):
        self.cur.execute("INSERT INTO binfo "
                "(f_id, author, imprintinfo, callnumber, year, page) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (f_id, author, imprintinfo, callnumber, year, page))
        self.db.commit()
        
    def addEBook(self, f_id, title, author, year, page):
        self.cur.execute("INSERT INTO einfo "
                "(f_id, title, author, year, page) "
                "VALUES (?, ?, ?, ?, ?)",
                (f_id, title, author, year, page))
        self.db.commit()
        
    def addImage(self, f_id, dimensions):
        self.cur.execute("INSERT INTO iinfo "
                "(f_id, dimensions) "
                "VALUES (?, ?)",
                (f_id, dimensions))
        self.db.commit()
        
    def addMusic(self, f_id, title, artist, album, date, tracknumber, genre, bitrate, frequence, length):
        self.cur.execute("INSERT INTO minfo "
                "(f_id, title, artist, album, date, tracknumber, genre, bitrate, frequence, length) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (f_id, title, artist, album, date, tracknumber, genre, bitrate, frequence, length))
        self.db.commit()
        
    def addVideo(self, f_id, title, length, dimensions):
        self.cur.execute("INSERT INTO vinfo "
                "(f_id, title, length, dimensions) "
                "VALUES (?, ?, ?, ?)",
                (f_id, title, length, dimensions))
        self.db.commit()
        
    def addTags(self, name):
        self.cur.execute("INSERT INTO tags (name) VALUES (?)", name)
        self.db.commit()
        
    #Updating functions
    
    def updateDir(self, id, up_id, name, datec, datem, datea, datei, desc):
        self.cur.execute("UPDATE dirs SET "
                "up_id=?, name=?, datecreate=?, datemodify=?, dateaccess=?, dateaddcat=?, description=? "
                "WHERE id=?",
                (up_id, name, datec, datem, datea, datei, desc, id))
        self.db.commit()
        
    def updateFile(self, id, up_id, name, size, datec, datem, datea, datei, type):
        self.cur.execute("UPDATE files SET "
                "up_id=?, name=?, size=?, datecreate=?, datemodify=?, dateaccess=?, dateaddcat=?, type=? "
                "WHERE id=?",
                (up_id, name, size, datec, datem, datea, datei, type, id))
        self.db.commit()
        
    def updateBook(self, f_id,author, imprintinfo, callnumber, year, page):
        self.cur.execute("UPDATE binfo SET "
                "author=?, imprintinfo=?, callnumber=?, year=?, page=? "
                "WHERE f_id=?",
                (author, imprintinfo, callnumber, year, page, f_id))
        self.db.commit()
        
    def updateEBook(self, f_id, title, author, year, page):
        self.cur.execute("UPDATE einfo SET "
                "title=?, author=?, year=?, page=? "
                "WHERE f_id=?",
                (title, author, year, page, f_id))
        self.db.commit()
        
    def updateImage(self, f_id, dimensions):
        self.cur.execute("UPDATE iinfo SET "
                "dimensions=? "
                "WHERE f_id=?",
                (dimensions, f_id))
        self.db.commit()
        
    def updateMusic(self, f_id, title, artist, album, year, track, genre, comment, bitrate, frequence, duration):
        self.cur.execute("UPDATE minfo SET "
                "title=?, artist=?, album=?, year=?, track=?, genre=?, "
                "comment=?, bitrate=?, frequence=?, duration=? "
                "WHERE f_id=?",
                (title, artist, album, year, track, genre, comment, bitrate, frequence, duration, f_id))
        self.db.commit()
        
    def updateVideo(self, f_id, title, duration, dimensions):
        self.cur.execute("UPDATE vinfo SET "
                "title=?, duration=?, dimensions=? "
                "WHERE f_id=?",
                (title, duration, dimensions, f_id))
        self.db.commit()
        
    # Deleting functions
    
    def delDir(self, id):
        self.cur.execute("DELETE FROM dirs WHERE id=%s"% id)
        self.cur.execute("DELETE FROM tagdirs WHERE d_id=%s"% id)
        self.db.commit()
        
    def delFile(self, id):
        type = self.cur.execute("SELECT type FROM files WHERE id=%s"% id).fetchone()[0]
        self.cur.execute("DELETE FROM files WHERE id=%s"% id)
        self.cur.execute("DELETE FROM tagfiles WHERE f_id=%s"% id)
        self.db.commit()
        return type
        
    def delInfo(self, f_id, type):
        types={"book":"binfo", "ebook":"einfo", "image":"iinfo",
                "music":"minfo", "video":"vinfo", "other":None}
        table = types[type]
        if table != None:
            self.cur.execute("DELETE FROM %s WHERE f_id=%s"% (table, f_id))
            self.db.commit()
        
    def delTag(self, id):
        self.cur.execute("DELETE FROM tags WHERE id=%s"% id)
        self.cur.execute("DELETE FROM tagdirs WHERE t_id=%s"% id)
        self.cur.execute("DELETE FROM tagfiles WHERE t_id=%s"% id)
        self.db.commit()
        
    # Searching by up_id
    
    def searchFile(self, up_id):
        self.cur.execute("SELECT id FROM files WHERE up_id=%s"% up_id)
        return self.cur.fetchall()
        
    def searchDir(self, up_id):
        self.cur.execute("SELECT id FROM dirs WHERE up_id=%s"% up_id)
        return self.cur.fetchall()
        
    def takeDirUpId(self, id):
        self.cur.execute("SELECT up_id FROM dirs WHERE id=%s"% id)
        return self.cur.fetchone()[0]
        
    # Showing directories
    
    def listDirById(self, id):
        dirs = {}
        self.cur.execute("SELECT id, name FROM dirs WHERE up_id=%s"% id)
        for i in self.cur.fetchall():
            dirs[i[1]]=i[0]
        
        files = {}
        self.cur.execute("SELECT id, name FROM files WHERE up_id=%s"% id)
        for i in self.cur.fetchall():
            files[i[1]]=i[0]
        
        return [dirs, files]
        
    # Taking info
    
    def info(self, id, type):
        infos = {}
        self.cur.execute("SELECT * FROM %s WHERE id=%s"% (type, id))
        data = self.cur.fetchone()
        keys = []
        colnames = self.cur.execute("PRAGMA TABLE_INFO(%s)"% type)
        for i in colnames.fetchall():
            keys.append(i[1])
        i=0
        while i<len(keys):
            infos[keys[i]] = data[i]
            i += 1
        infos["up_id"] = self.genAddress(infos["up_id"])            
        return infos
        
    def detailInfo(self, id, type):
        infos = {}
        types={"book":"binfo", "ebook":"einfo", "image":"iinfo",
                "music":"minfo", "video":"vinfo"}
        self.cur.execute("SELECT * FROM %s WHERE f_id=%s"% (types[type], id))
        data = self.cur.fetchone()
        keys = []
        colnames = self.cur.execute("PRAGMA TABLE_INFO(%s)"% types[type])
        for i in colnames.fetchall():
            keys.append(i[1])
        i=0
        while i<len(keys):
            infos[keys[i]] = data[i]
            i += 1
        return infos
        
    # Generating address
    
    def genAddress(self, up_id):
        upDirs = []
        address = "/"
        while up_id != 0:
            self.cur.execute("SELECT up_id, name FROM dirs WHERE id=%s"% up_id)
            up_id, name = self.cur.fetchone()
            upDirs.append(name)
        upDirs.reverse()
        for i in upDirs:
            address += i + "/"
        return address
