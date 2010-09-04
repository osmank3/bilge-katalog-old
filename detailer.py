#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database

from warnings import simplefilter # for ignoriny DeprecationWarning.
simplefilter("ignore", DeprecationWarning)

import kaa.metadata as Meta
import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

DB = database.dataBase()

def getKeys(type):
    infos = {}
    Query = database.EditQuery()
    Query.setStatTrue("pragma")
    Query.setTables([type])
    Request = DB.execute(Query.returnQuery())
    for i in Request:
        if i[1] != "f_id":
            if i[2] == "INTEGER":
                infos[i[1]] = 0
            else:
                infos[i[1]] = ""
    return infos
    
def loop4infos(info, infos): # info from file, infos to database
    for i in infos.keys():
        try:
            if info.has_key(i):
                if type(infos[i]) == int:
                    infos[i] = int(info[i][0])
                else:
                    infos[i] = info[i][0]
        except ValueError:
            pass
    return infos

def infoFile(file):
    infos = {}
    info = Meta.parse(file)
    for i in info.keys():
        if info[i]:
            infos[i] = info[i]
    return infos

def mp3Tags(file):
    infos = getKeys("minfo")
    info = MP3(file, EasyID3)
    infos["bitrate"] = info.info.bitrate
    infos["samplerate"] = info.info.sample_rate
    infos["length"] = int(float(info.info.length))
    infos = loop4infos(info, infos)
    return infos
    
def oggTags(file):
    infos = getKeys("minfo")
    info = mutagen.File(file)
    infos["bitrate"] = info.info.bitrate
    infos["samplerate"] = info.info.sample_rate
    infos["length"] = int(float(info.info.length))
    infos = loop4infos(info, infos)
    return infos
    
def videoInfo(file):
    infos = getKeys("vinfo")
    info = infoFile(file)
    infos = loop4infos(info, infos)
    return infos
    
def imageInfo(file):
    infos = getKeys("iinfo")
    info = infoFile(file)
    infos = loop4infos(info, infos)
    return infos
