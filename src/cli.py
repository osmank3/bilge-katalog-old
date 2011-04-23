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
                        
    class progress(object):
        """İlerleme yüzdesini göstermek için yazılan nesne."""
        numOfItems = 0
        curNum = 0
        
        def __init__(self, address=None):
            """İlerleme yüzdesi oluşturma sınıfı
            
            progress(address=None)"""
            if address:
                self.numOfItems = self.getNumOfItems(address) + 1
            else:
                self.numOfItems = 1
                
        def getNumOfItems(self, address):
            """Verilen adresteki dosya ve dizinlerin sayısını dönen fonksiyon.
            
            getNumOfItems(address)"""
            oldDir = os.getcwd()
            os.chdir(address)
            dirList = os.listdir("./")
            numOfItems = len(dirList)
            
            for i in dirList:
                if os.path.isdir(i):
                    numOfItems += self.getNumOfItems(i)
                    
            os.chdir(oldDir)
            return numOfItems
            
        def increase(self):
            """İşlenenlerin sayısını bir artıran fonksiyon."""
            self.curNum += 1
            self.printPercent()
            
        def getPercent(self):
            """İşlenenlerin yüzdesini dönen fonksiyon."""
            percent = 100 * self.curNum / self.numOfItems
            return percent
            
        def printPercent(self):
            if self.getPercent() == 100:
                sys.stdout.write("\r" + str(self.getPercent()) + " % "
                                    + _("Finished\n"))
                sys.stdout.flush()
            else:
                sys.stdout.write("\r" + str(self.getPercent()) + " %")
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
                        progressItem = progress(parameters["path"])
                    else:
                        isContinue = raw_input(_("Eksik bağımlılıklar var. Bu durum dosyalarda bilgi eksikliğine yol açabilir.\nYinede devam edilsin mi? (e/h): "))
                        if isContinue.lower() in [_("e"), _("evet")]:
                            catalog.setAddress(parameters["path"])
                            progressItem = progress(parameters["path"])
                        else:
                            print _("İşlem iptal edildi.")
                            continue
                else:
                    progressItem = progress()
                
                inserting.createDir(catalog, progressItem)
                Exp.curItemList = Exp.fillList()
                
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
                    progressItem = progress(parameters["path"])
                else:
                    isContinue = raw_input(_("Eksik bağımlılıklar var. Bu durum dosyalarda bilgi eksikliğine yol açabilir.\nYinede devam edilsin mi? (e/h): "))
                    if isContinue.lower() in [_("e"), _("evet")]:
                        directory.setAddress(parameters["path"])
                        progressItem = progress(parameters["path"])
                    else:
                        print _("İşlem iptal edildi.")
                        continue
            else:
                progressItem = progress()
            
            inserting.createDir(directory, progressItem)
            Exp.curItemList = Exp.fillList()
            
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
                    
            progressItem = progress()
            
            if fileDetail.getInfos():
                inserting.createFile(fileItem, progressItem, fileDetail)
            else:
                inserting.createFile(fileItem, progressItem)
                
            Exp.curItemList = Exp.fillList()
            
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
            
        elif command == "update":
            if len(additions)>0:
                name = " ".join(additions)
                for j in Exp.curItemList:
                    if j.name == name:
                        j.setDetail()
                        infoKeys = ["name","size","datecreate","datemodify",
                                    "dateaccess","dateinsert","type","description"]
                        for i in parameters.keys():
                            if i in infoKeys:
                                j.info[i] = parameters[i]
                            else:
                                j.detail[i] = parameters[i]
                                
                        bridge.ItemWorks().updateItem(j)
                        Exp.curItemList = Exp.fillList()
                    
        elif command == "whereis":
            if len(additions)>0:
                text = " ".join(additions)
                itemList = bridge.ItemWorks().search(text)
                for i in itemList:
                    print i.address + i.name
        
        elif command == "mv":
            pass#taşımak için
                    
        elif command == "cp":
            pass#kopyalamak için
                
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
