#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
from bilge_katalog.bridge import *
from PyQt4 import QtCore
from PyQt4 import QtGui

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

class ItemQt(Item, QtGui.QListWidgetItem):
    """Bilge-katalog Qt arayüzde dosya ve dizinlerin bilgilerini tutmak için nesne.
    
    Değişkenler:
    no -- int
    name -- str
    form -- "file" or "directory"
    address -- str "/foo/bar"
    updir -- Item
    """
    def Item2QtItem(self, item):
        """Item'leri ItemQtList'e dönüştüren fonksiyondur."""
        attributes = ["no", "name", "form", "address", "updir", "info", "detail"]
        for i in attributes:
            if i in dir(item):
                setattr(self, i, getattr(item, i))

class RootItemQt(RootItem, QtGui.QListWidgetItem):
    """Kök dizini belirtmek için oluşturulmuş özel nesne"""
    pass

def List2QtItem(itemList=None):
    """Item listesini ItemQt listesine çevirir."""
    newItemList = []
    
    for i in itemList:
        tempItem = ItemQt()
        tempItem.Item2QtItem(i)
        newItemList.append(tempItem)
        
    return newItemList

class ExploreQt(Explore):
    """Bilge-Katalog Qt arayüz için dizinlerde gezinme sınıfı."""
    def __init__(self):
        """Gezinme sınıfı için kök dizini ve içeriğinin listesinin
        hazırlanması."""
        self.curItem = RootItemQt()
        self.refresh()
        
    def refresh(self):
        self.curItemList = self.fillListQt()
        
    def fillListQt(self, item=None):
        """Qt arayüz için dizin içi listesi oluşturan fonksiyondur."""
        itemList = self.fillList(item)
        return List2QtItem(itemList)
        
class ItemWorksQt(ItemWorks):
    """Qt arayüzde Dosya/Dizin işlemleri için oluşturulan sınıftır."""
    def searchQt(self, text):
        """Qt arayüzde veritabanında arama yapmak için fonksiyon"""
        itemList = self.search(text)
        return List2QtItem(itemList)
        