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

class DB:
    def __init__(self):
        creating = False
        if not os.path.isfile(DBFile):
            creating = True
        self.db = sqlite3.connect(DBFile)
        self.cur = self.db.cursor()
        if creating:
            self.createTables()
        
    def createTables(self):
        self.cur.execute("CREATE TABLE dirs ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "up_id INTEGER, "
               "name TEXT, "
               "date TEXT, "
               "description TEXT)")
               
        self.cur.execute("CREATE TABLE files ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "up_id INTEGER, "
               "name TEXT, "
               "size INTEGER, "
               "date TEXT, "
               "type TEXT)")
               
        self.cur.execute("CREATE TABLE minfo ("
               "f_id INTEGER PRIMARY KEY, "
               "title TEXT, "
               "artist TEXT, "
               "album TEXT, "
               "year INTEGER, "
               "track INTEGER, "
               "genre TEXT, "
               "comment TEXT, "
               "bitrate INTEGER, "
               "frequence INTEGER, "
               "duration TEXT)")

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
               "dimensions TEXT,"
               "createdate DATE)")

        self.cur.execute("CREATE TABLE vinfo ("
               "f_id INTEGER PRIMARY KEY, "
               "title TEXT, "
               "duration TEXT, "
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
    
    #Adding functions
        
    def addDir(self, up_id, name, date, desc=''):
        self.cur.execute("INSERT INTO dirs "
                "(up_id, name, date, description) "
                "VALUES (?, ?, ?, ?)",
                (up_id, name, date, desc))
        self.db.commit()
        id = self.cur.execute("SELECT max(id) FROM dirs").fetchall()
        return id[0][0]
        
    def addFile(self, up_id, name, size, date, type):
        self.cur.execute("INSERT INTO files "
                "(up_id, name, size, date, type) "
                "VALUES (?, ?, ?, ?, ?)",
                (up_id, name, size, date, type))
        self.db.commit()
        
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
        
    def addImage(self, f_id, dimensions, createdate):
        self.cur.execute("INSERT INTO iinfo "
                "(f_id, dimensions, createdate) "
                "VALUES (?, ?, ?)",
                (f_id, dimensions, createdate))
        self.db.commit()
        
    def addMusic(self, f_id, title, artist, album, year, track, genre, comment, bitrate, frequence, duration):
        self.cur.execute("INSERT INTO minfo "
                "(f_id, title, artist, album, year, track, genre, comment, bitrate, frequence, duration) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (f_id, title, artist, album, year, track, genre, comment, bitrate, frequence, duration))
        self.db.commit()
        
    def addVideo(self, f_id, title, duration, dimensions):
        self.cur.execute("INSERT INTO vinfo "
                "(f_id, title, duration, dimensions) "
                "VALUES (?, ?, ?, ?)",
                (f_id, title, duration, dimensions))
        self.db.commit()
        
    def addTags(self, name):
        self.cur.execute("INSERT INTO tags (name) VALUES (?)", name)
        self.db.commit()
        
    #Updating functions
    
    def updateDir(self, id, up_id, name, date, desc):
        self.cur.execute("UPDATE dirs SET "
                "up_id=?, name=?, date=?, description=? "
                "WHERE id=?",
                (up_id, name, date, desc, id))
        self.db.commit()
        
    def updateFile(self, id, up_id, name, size, date, type):
        self.cur.execute("UPDATE files SET "
                "up_id=?, name=?, size=?, date=?, type=? "
                "WHERE id=?",
                (up_id, name, size, date, type, id))
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
        
    def updateImage(self, f_id, dimensions, createdate):
        self.cur.execute("UPDATE iinfo SET "
                "dimensions=?, createdate=? "
                "WHERE f_id=?",
                (dimensions, createdate, f_id))
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
        self.cur.execute("DELETE FROM files WHERE id=%s"% id)
        self.cur.execute("DELETE FROM tagfiles WHERE f_id=%s"% id)
        self.db.commit()
        
    def delInfo(self, f_id, type):
        types={"book":"binfo", "ebook":"einfo", "image":"iinfo",
                "music":"minfo", "video":"vinfo"}
        self.cur.execute("DELETE FROM %s WHERE f_id=%s"%
                (types[type], f_id))
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
        
    # Showing directories
    
    def showDir(self, id):
        dirs = {}
        self.cur.execute("SELECT id, name FROM dirs WHERE up_id=%s"% id)
        for i in self.cur.fetchall():
            dirs[i[0]]=i[1]
        
        files = {}
        self.cur.execute("SELECT id, name FROM files WHERE up_id=%s"% id)
        for i in self.cur.fetchall():
            files[i[0]]=i[1]
        
        return [dirs, files]
