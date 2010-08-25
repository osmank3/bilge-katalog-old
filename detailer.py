#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database
import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

DB = database.DB()

mkeys = ["title", "artist", "album", "date", "tracknumber",
            "genre", "bitrate", "frequence", "length"]

def mp3Tags(file):
    infos = {}
    info = MP3(file, EasyID3)
    infos["bitrate"] = info.info.bitrate
    infos["frequence"] = info.info.sample_rate
    infos["length"] = int(float(info.info.length))
    for i in info.keys():
        if i == "date" or i == "tracknumber":
            infos[i] = int(info[i][0])
        else:
            infos[i] = info[i][0]
    for i in mkeys:
        if infos.has_key(i) == 0:
            if i == "date" or i == "tracknumber":
                infos[i] = 0
            else:
                infos[i] = ""
    return infos
    
def oggTags(file):
    infos = {}
    info = mutagen.File(file)
    infos["bitrate"] = info.info.bitrate
    infos["frequence"] = info.info.sample_rate
    infos["length"] = int(float(info.info.length))
    for i in info.keys():
        if i == "date" or i == "tracknumber":
            infos[i] = int(info[i][0])
        else:
            infos[i] = info[i][0]
    for i in mkeys:
        if infos.has_key(i) == 0:
            if i == "date" or i == "tracknumber":
                infos[i] = 0
            else:
                infos[i] = ""
    return infos
    
def mp4Tags(file):
    infos = {}
