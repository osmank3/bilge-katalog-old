#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import sqlite3
import datetime

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
               "dateinsert TIMESTAMP, "
               "description TEXT)")
               
        self.cur.execute("CREATE TABLE files ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "up_id INTEGER, "
               "name TEXT, "
               "size INTEGER, "
               "datecreate TIMESTAMP, "
               "datemodify TIMESTAMP, "
               "dateaccess TIMESTAMP, "
               "dateinsert TIMESTAMP, "
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
               "samplerate INTEGER, "
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
               "width INTEGER, "
               "height INTEGER)")

        self.cur.execute("CREATE TABLE vinfo ("
               "f_id INTEGER PRIMARY KEY, "
               "title TEXT, "
               "length INTEGER, "
               "width INTEGER, "
               "height INTEGER)")

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
        self.cur.execute(query[0], query[1])
        if query[0].find("SELECT") == 0 or query[0].find("PRAGMA") == 0:
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
            self.keys = ""
            self.values = ""
            self.additions = []
            
    def setTables(self, tables): # [x1, x2, ...]
        self.table = ""
        for i in tables:
            self.table += str(i) + ", "
        self.table = self.table[:-2]
        
    def setKeys(self, lists): # [x1, x2, ...]
        self.keys = ""
        for i in lists:
            self.keys += i + ", "
        self.keys = self.keys[:-2]
        
    def setValues(self, lists): # [x1, x2, ...]
        self.values = ""
        self.additions = []
        for i in lists:
            if type(i) == int:
                self.values += str(i) + ", "
            elif type(i) == datetime.datetime:
                self.additions.append(i)
                self.values += "?, "
            else :
                try:
                    self.values += '"' + i + '", '
                except:
                    self.values += '"", '
        self.values = self.values[:-2]
        
        
    def setSet(self, setkeys): # {x1:y1, x2:y2, ...}
        self.set = ""
        for i in setkeys.keys():
            self.set += str(i) + "=" + str(setkeys[i]) + ", "
        self.set = self.set[:-2]
        
    def setSelect(self, selections): # [x1, x2, ...]
        self.select = ""
        for i in selections:
            self.select += str(i) + ", "
        self.select = self.select[:-2]
        
    def setWhere(self, where): # [{x1:y1}, op12, {x2:y2}, op23, ...]
        self.where = ""
        for i in where:
            if type(i) == dict:
                self.where += str(i.items()[0][0]) + "=" + str(i.items()[0][1])
            else:
                self.where += " " + str(i) + " "
                
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
            if self.table != "" or self.values != "" or self.keys != "":
                self.query += "INSERT INTO " + self.table
                self.query += " (" + self.keys + ") "
                self.query += " VALUES (" + self.values + ")"
            
        elif self.status["pragma"]:
            if self.table != "":
                self.query += "PRAGMA TABLE_INFO(" + self.table + ")"
            
    def returnQuery(self):
        self.setQuery()
        if self.query != "":
            return (self.query, self.additions)
        else:
            return False
            

