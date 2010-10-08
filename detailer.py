#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database
import re

from warnings import simplefilter # for ignoriny DeprecationWarning.
simplefilter("ignore", DeprecationWarning)

import kaa.metadata as Meta
import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from reportlab.pdfgen import canvas

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

DB = database.dataBase()

pdfpage = re.compile("/Count\s+(\d+)")
pdfauthor = re.compile("/Author\s+\((.*)\)")
pdftitle = re.compile("/Title\s+\((.*)\)")
pdfyear = re.compile("/CreationDate\s+\(D:(....)")

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
                    if type(info[i]) == list:
                        infos[i] = int(info[i][0])
                    else:
                        infos[i] = int(info[i])
                else:
                    if type(info[i]) == list:
                        infos[i] = info[i][0]
                    else:
                        infos[i] = info[i]
        except ValueError:
            pass
    return infos

def infoFile(file):
    infos = {}
    info = Meta.parse(file)
    for i in info.keys():
        if info[i]:
            infos[i] = info[i]
    try:
        video = info.video[0]
        for i in video.keys():
            if video[i]:
                infos[i] = video[i]
    except:
        pass
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
    
def musicInfo(file):
    infos = getKeys("minfo")
    info = infoFile(file)
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

def pdfInfo(file):
    infos = getKeys("ebook")
    pdf = canvas.Canvas(file)
    pdfMetaText = pdf.getpdfdata()
    if pdfauthor.findall(pdfMetaText)[0] != "anonymous":
        infos["author"] = pdfauthor.findall(pdfMetaText)[0]
    if pdftitle.findall(pdfMetaText)[0] != "untitled":
        infos["title"] = pdftitle.findall(pdfMetaText)[0]
    infos["year"] = int(pdfyear.findall(pdfMetaText)[0])
    pdffile = open(file, "rb", 1).read()
    pages = 0
    for match in pdfpage.finditer(pdffile):
        pages = int(match.group(1))
    infos["page"] = int(pages)
    return infos