#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import re
import readline #this is for history and editing line
import bridge
import inserting

#For using unicode utf-8
reload(sys).setdefaultencoding("utf-8")

#For multilanguage support
gettext.install("bilge-katalog", unicode=1)

parse1 = re.compile("([^\s]+=\"[^\"]*\")", re.IGNORECASE|re.UNICODE)
parse2 = re.compile("([^\s]+=[^\s]+)", re.IGNORECASE|re.UNICODE)
parse3 = re.compile("(\"[^\"]*\")", re.IGNORECASE|re.UNICODE)
    
def parser(entry):
    try:
        command = entry.split()[0]
    except IndexError:
        return "", None, None
    entry = entry[len(command):]
    parameters = {}
    additions = []
    address = []
    entry = entry.replace("'","\"")
    parsed1 = parse1.findall(entry)
    for i in parsed1:
        entry = entry.replace(i,"")
    parsed2 = parse2.findall(entry)
    for i in parsed2:
        entry = entry.replace(i,"")
    parsed = parsed1 + parsed2
    for i in parsed:
        key, value = i.split("=")
        value = value.replace("\"","")
        parameters[key]=value
    for i in parse3.findall(entry):
        value = i.replace("\"","")
        additions.append(value)
    for i in additions:
        entry = entry.replace(i,"")
    additions += entry.split()
    if '""' in additions:
        additions.remove('""')
    return command, parameters, additions
    
def parseAddress(address):
    addressList = []
    if "/" in address:
        if address.find("/") == 0:
            addressList.append("/")
        parts = address.split("/")
        for i in parts:
            if i != "":
                addressList.append(i)
    else:
        addressList.append(address)
    return addressList
    
def mainloop():
    Exp = bridge.Explore()
    
    def changeAddress(text):
        for i in parseAddress(text):
            if i == "/":
                Exp.chdir(bridge.RootItem())
            elif i == "..":
                Exp.turnUp()
            else:
                for j in Exp.curItemList:
                    if j.name == i:
                        Exp.chdir(j)
                        break
    
    print _("Welcome to bilge-katalog!\
\nFor helping only write 'help' and press Enter")
    QUIT = False
    while QUIT == False:
        entry = raw_input(">> %s # "% Exp.curItem.name)
        entry = entry.decode('utf-8')
        command, parameters, additions = parser(entry)
        
        if command == "quit" or command == "exit":
            QUIT = True
            
        elif command == "cd":
            if len(additions)>0:
                name = " ".join(additions)
                changeAddress(name)
            
        elif command == "info":
            if len(additions)>0:
                name = " ".join(additions)
                for j in Exp.curItemList:
                    if j.name == name:
                        print j.textTypeInfo()
                
        elif command == "ls":
            if len(additions)>0:
                name = " ".join(additions)
                oldAddress = Exp.curItem.address + "/" + Exp.curItem.name
                changeAddress(name)
                Exp.ls()
                changeAddress(oldAddress)
            else:
                Exp.ls()
            
        elif command == "rm":
            if len(additions)>0:
                name = " ".join(additions)
                for j in Exp.curItemList:
                    if j.name == name:
                        bridge.ItemWorks().delItem(j)
                        Exp.curItemList = Exp.fillList()
            
        elif command == "search":
            if len(additions)>0:
                text = " ".join(additions)
                itemList = bridge.ItemWorks().search(text)
                for i in itemList:
                    print i.address + ":"
                    print i.textTypeInfo()
                    
        elif command == "status":
            print _("Dosyadan metadata eldesi: ") + str(inserting.EnableMetaData)
            print _("Dosyadan detaylı Mp3 bilgisi: ") + str(inserting.EnableMp3)
            print _("Dosyadan detaylı pdf bilgisi: ") + str(inserting.EnablePdf)
            
        elif command == "whereis":
            if len(additions)>0:
                text = " ".join(additions)
                itemList = bridge.ItemWorks().search(text)
                for i in itemList:
                    print i.address + i.name
                    
        elif command == "mkcat":
            pass#katalog oluşturma
                
        elif command == "mkdir":
            pass#dizin oluşturma
            
        elif command == "mkfile":
            pass#dosya oluşturma
        
        elif command == "update":
            pass#bilgileri güncellemek için
                    
        elif command == "mv":
            pass#taşımak için
                    
        elif command == "cp":
            pass#copyalamak için
                
        elif command == "lend":
            pass#ödünç vermek için
                    
        elif command == "tkback":
            pass#ödüncü geri almak için
                
        elif command == "reserve":
            pass#ayırmak için
                    
        elif command == "user":
            action = additions[0]
            additions.pop(0)
            if action == "add":
                pass#kişi ekleme
            elif action == "update" and len(additions)>0:
                pass#kişi güncelleme
            elif action == "info" and len(additions)>0:
                pass#kişi bilgileri
                

    print _("Thanks for using bilge-katalog")
    
if __name__ == "__main__":
    mainloop()
