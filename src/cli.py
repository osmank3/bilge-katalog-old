#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import re
import readline #this is for history and editing line
import time
import bridge
import inserting
from threading import Thread

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
                        
    class thread(Thread):
        def __init__(self, Progress):
            Thread.__init__(self)
            self.progress = Progress
            
        def run(self):
            while self.progress.getPercent() < 101:
                time.sleep(0.1)
                if self.progress.getPercent() == 100:
                    sys.stdout.write("\r" + str(self.progress.getPercent()) + " % "
                                     + _("Finished\n"))
                    sys.stdout.flush()
                    break
                else:
                    sys.stdout.write("\r" + str(self.progress.getPercent()) + " %")
                    sys.stdout.flush()
    
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
                    if True in status():
                        catalog.setAddress(parameters["path"])
                        progressItem = inserting.progress(parameters["path"])
                    else:
                        isContinue = raw_input(_("Eksik bağımlılıklar var. Bu durum dosyalarda bilgi eksikliğine yol açabilir.\nYinede devam edilsin mi? (e/h): "))
                        if isContinue.lower() in [_("e"), _("evet")]:
                            catalog.setAddress(parameters["path"])
                            progressItem = inserting.progress(parameters["path"])
                        else:
                            print _("İşlem iptal edildi.")
                            continue
                else:
                    progressItem = inserting.progress()
                    
                process = thread(progressItem)
                process.start()
                
                inserting.createDir(catalog, progressItem)
                Exp.curItemList = Exp.fillList()
                
                process.join()
                print _("%s kataloğu oluşturuldu."% name)
                
        elif command == "mkdir":
            name = " ".join(additions)
            if "desc" in parameters.keys():
                desc = parameters["desc"]
            else:
                desc = ""
            directory = inserting.Item("directory", {"up_id":Exp.curItem.no,
                                                     "name":name,
                                                     "description":desc})
            if "path" in parameters.keys():
                if True in status():
                    directory.setAddress(parameters["path"])
                    progressItem = inserting.progress(parameters["path"])
                else:
                    isContinue = raw_input(_("Eksik bağımlılıklar var. Bu durum dosyalarda bilgi eksikliğine yol açabilir.\nYinede devam edilsin mi? (e/h): "))
                    if isContinue.lower() in [_("e"), _("evet")]:
                        directory.setAddress(parameters["path"])
                        progressItem = inserting.progress(parameters["path"])
                    else:
                        print _("İşlem iptal edildi.")
                        continue
            else:
                progressItem = inserting.progress()
                
            process = thread(progressItem)
            process.start()
            
            inserting.createDir(directory, progressItem)
            Exp.curItemList = Exp.fillList()
            
            process.join()
            print _("%s dizini oluşturuldu."% name)
            
        elif command == "mkfile":
            name = " ".join(additions)
            
            fileItem = inserting.Item("file", {"up_id":Exp.curItem.no,
                                               "name":name})
            
            if "path" in parameters.keys():
                if True in status():
                    fileItem.setAddress(parameters["path"])
                    fileDetail = inserting.DetailItem(name=name, address=parameters["path"])
                else:
                    isContinue = raw_input(_("Eksik bağımlılıklar var. Bu durum dosyada bilgi eksikliğine yol açabilir.\nYinede devam edilsin mi? (e/h): "))
                    if isContinue.lower() in [_("e"), _("evet")]:
                        fileItem.setAddress(parameters["path"])
                        fileDetail = inserting.DetailItem(name=name, address=parameters["path"])
                    else:
                        print _("İşlem iptal edildi.")
                        continue
            else:
                if parameters["type"] == "book":
                    fileDetail = inserting.DetailItem(name=name, info=parameters, book=True)
                else:
                    fileDetail = inserting.DetailItem(name=name, info=parameters)
                    
            progressItem = inserting.progress()
                
            process = thread(progressItem)
            process.start()
            
            if fileDetail.getInfos():
                inserting.createFile(fileItem, progressItem, fileDetail)
            else:
                inserting.createFile(fileItem, progressItem)
                
            Exp.curItemList = Exp.fillList()
            
            process.join()
            print _("%s dosyası oluşturuldu."% name)
                
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
