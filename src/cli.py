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

parse1 = re.compile("-([^\s]+='[^']*'|[^\s]+=\"[^\"]*\"|[^\s]+=[^\s]+|[^\s]+\s'[^']*'|[^\s]+\s\"[^\"]*\"|[^\s]+\s[^\s]+)", re.IGNORECASE|re.UNICODE)
parse2 = re.compile("(\"[^\"]*\"|'[^']*'|[^\s]+)", re.IGNORECASE|re.UNICODE)
    
def parser(entry):
    try:
        templist = entry.split()
        command = templist[0]
        entry = " ".join(templist[1:])
    except IndexError:
        return "", None, None
    parameters = {}
    additions = []
    address = []
    
    parsed = parse1.findall(entry)
    for i in parsed:
        if "=" in i:
            key, value = i.split("=")
        elif " " in i:
            splited = i.split(" ")
            key = splited[0]
            value = " ".join(splited[1:])
        if value[0] == "\"":
            value = value[1:-1]
        elif value[0] == "'":
            value = value[1:-1]
        
        parameters[key]=value
        
        #delete parameters from entry
        entry = entry.replace("-%s"% i, "")
    
    for i in parse2.findall(entry):
        if i[0] == "\"":
            value = i[1:-1]
        elif i[0] == "'":
            value = i[1:-1]
        else:
            value = i
        
        additions.append(value)
        
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
    
def status():
    returnStat = []
    if not inserting.EnableMetaData:
        returnStat.append(_("Dosyaların ayrıntılı bilgileri elde edilemeyecek!"))
    if not inserting.EnablePdf:
        returnStat.append(_("E-kitapların ayrıntılı bilgileri elde edilemeyecek!"))
    if not inserting.EnableMp3:
        returnStat.append(_("MP3 dosyalarının ayrıntılı bilgilerinde eksiklik olabilir!"))
    if len(returnStat) == 0:
        returnStat.append(True)
    return returnStat
    
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
    
    print _("Welcome to bilge-katalog!\n\
           \rFor helping only write 'help' and press Enter")
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
                    
        elif command == "mkcat":
            if len(additions)>0:
                name = " ".join(additions)
                if "desc" in parameters.keys():
                    desc = parameters["desc"]
                else:
                    desc = ""
                catalog = inserting.Item("directory", {"up_id":0,
                                                       "name":name,
                                                       "description":desc})
                if "path" in parameters.keys():
                    catalog.setAddress(parameters["path"])
                inserting.createDir(catalog)
                Exp.curItemList = Exp.fillList()
                print _("%s kataloğu oluşturuldu."% name)
                
        elif command == "mkdir":
            if len(additions)>0:
                name = " ".join(additions)
                if "desc" in parameters.keys():
                    desc = parameters["desc"]
                else:
                    desc = ""
                directory = inserting.Item("directory", {"up_id":Exp.curItem.no,
                                                         "name":name,
                                                         "description":desc})
                if "path" in parameters.keys():
                    directory.setAddress(parameters["path"])
                inserting.createDir(directory)
                Exp.curItemList = Exp.fillList()
                print _("%s dizini oluşturuldu."% name)
            
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
            for i in status():
                if i == True:
                    print _("Bütün bağımlılıklar sağlanmış durumda.")
                else:
                    print i
            
        elif command == "whereis":
            if len(additions)>0:
                text = " ".join(additions)
                itemList = bridge.ItemWorks().search(text)
                for i in itemList:
                    print i.address + i.name
            
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
