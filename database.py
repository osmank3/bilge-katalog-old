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

DBFile = ":memory:"#hız için şimdilik "database.db" yerine kullanalım.

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
               "date DATE, "
               "description TEXT)")
               
        self.cur.execute("CREATE TABLE files ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "up_id INTEGER, "
               "name TEXT, "
               "size INTEGER, "
               "date DATE, "
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
               
