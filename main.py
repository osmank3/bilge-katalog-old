#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import gettext
import database
import libilge
import datetime
import re
import copy
import readline #this is for history and editing line

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
    
DB = database.dataBase()
EXP = libilge.explore()

def mainloop():
    print _("Welcome to bilge-katalog!\
\nFor helping only write 'help' an press Enter")
    QUIT = False
    while QUIT == False:
        entry = raw_input(">>> ")
        entry = entry.decode('utf-8')
        command, parameters, additions = parser(entry)
        
        #print command , parameters , additions
        
        if command == "help":
            if len(additions)>0:
                if additions[0] == "cd":
                    print "cd OPTS      " + _("changing current directory")
                    print _("Usage:")
                    print "cd id=ID     " + _("change current directory which id is ID")
                    print "cd NAME      " + _("change current directory which name is NAME")
                    
                elif additions[0] == "cp":
                    print "cp OPTS      " + _("copy files and directories")
                    print _("Usage:")
                    print "cp NAME to=ADDRESS     " + _("copy NAME to ADDRESS")
                    
                elif additions[0] == "info":
                    print "info OPTS    " + _("informations about file or directory")
                    print _("Usage:")
                    print "info NAME    " + _("informations about NAME")
                    
                elif additions[0] == "lend":
                    print "lend OPTS    " + _("lending file or directory")
                    print _("Usage:")
                    print "lend NAME to=USERID    " + _("NAME lending to USERID")
                    print "lend NAME              " + _("NAME lending to reserved user")
                    
                elif additions[0] == "ls":
                    print "ls OPTS      " + _("listing directory")
                    print _("Usage:")
                    print "ls id=ID     " + _("list directory which id is ID")
                    print "ls NAME      " + _("list directory which name is NAME")
                    
                elif additions[0] == "mkcat":
                    print "mkcat OPTS   " + _("creating catalog.")
                    print _("Usage:")
                    print "mkcat name=NAME desc=DESCRIPTIONS dir=DIRECTORY\n\t" + \
                            _("create catalog, NAME is name of catalog") + "\n\t" + \
                            _("DESCRIPTIONS is description of catalog (optional)") + \
                            "\n\t" + _("DIRECTORY for creating catalog (optional)")
                            
                elif additions[0] == "mkfile":
                    print "mkdir OPTS   " + _("creating a directory.")
                    print _("Usage:")
                    print "mkdir name=NAME desc=DESCRIPTIONS dir=DIRECTORY\n\t" + \
                            _("create directory, NAME is name of directory") + "\n\t" + \
                            _("DESCRIPTIONS is description of directory (optional)") + \
                            "\n\t" + _("DIRECTORY for creating directory (optional)")
                    
                elif additions[0] == "mkfile":
                    print "mkfile OPTS  " + _("creating a file.")
                    print _("Usage:")
                    print "mkfile NAME type=TYPE address=ADDRESS\n\t" + \
                            _("create file, NAME is name of file") + "\n\t" + \
                            _("TYPE is type of file (optional)") + "\n\t" + \
                            _("ADDRESS for creating file (optional)")
                            
                elif additions[0] == "mv":
                    print "mv OPTS      " + _("move files and directories")
                    print _("Usage:")
                    print "mv NAME to=ADDRESS     " + _("move NAME to ADDRESS")
                    
                elif additions[0] == "reserve":
                    print "reserve OPTS " + _("reserving file or directory")
                    print _("Usage:")
                    print "reserve NAME to=USERID   " + _("NAME reserving to USERID")
                elif additions[0] == "rm":
                    print "rm OPTS      " + _("removing file")
                    print _("Usage:")
                    print "rm id=ID     " + _("remove file which id is ID")
                    print "rm NAME      " + _("remove file which name is NAME")
                    
                elif additions[0] == "rmdir":
                    print "rmdir OPTS   " + _("removing directory")
                    print _("Usage:")
                    print "rmdir id=ID  " + _("remove directory which id is ID")
                    print "rmdir NAME   " + _("remove directory which name is NAME")
                    
                elif additions[0] == "search":
                    print "search OPTS  " + _("searching for entry")
                    print _("Usage:")
                    print "search ENTRY   " + _("search for ENTRY and print all informations of founded")
                    
                elif additions[0] == "tkback":
                    print "tkback OPTS  " + _("take back borrowed file or directory")
                    print _("Usage:")
                    print "tkback NAME  " + _("take back borrowed NAME")
                    
                elif additions[0] == "update":
                    print "update OPTS  " + _("updating files or directories informations")
                    print _("Usage:")
                    print "update NAME KEY=VALUE    " + _("update NAME's VALUE of KEY")
                    
                elif additions[0] == "user":
                    print "user OPTS    " + _("user actions")
                    print _("Usage:")
                    print "user add name=NAME surname=SURNAME ...\n\t" + \
                        _("add user with NAME SURNAME ... informations")
                    print "user del ID  " + _("Delete which user's id is ID")
                    print "user info ID " + _("Information about which user id is ID")
                    print "user update ID KEY=VALUE     " + _("update ID's VALUE of KEY")
                    print "user search ENTRY    " + _("search for ENTRY and print all informations of founded")
                    print "user search name=NAME surname=SURNAME ...\n\t" + \
                        _("search for which name is NAME and which surname is SURNAME")
                    
                elif additions[0] == "whereis":
                    print "whereis OPTS " + _("searching for entry and return theirs address")
                    print _("Usage:")
                    print "whereis ENTRY    " + _("search for ENTRY en print addresses of founded")
                    
            else:
                print _("Useful commands:")
                print "cd OPTS      " + _("changing current directory")
                print "cp OPTS      " + _("copy files and directories")
                print "exit         " + _("quiting on application")
                print "help OPTS    " + _("this help or using details of command")
                print "info OPTS    " + _("informations about file or directory")
                print "lend OPTS    " + _("lending file or directory")
                print "ls OPTS      " + _("listing directory")
                print "mkcat OPTS   " + _("creating catalog.")
                print "mkdir OPTS   " + _("creating a directory.")
                print "mkfile OPTS  " + _("creating a file.")
                print "mv OPTS      " + _("move files and directories")
                print "quit         " + _("quiting on application")
                print "reserve OPTS " + _("reserving file or directory")
                print "rm OPTS      " + _("removing file")
                print "rmdir OPTS   " + _("removing directory")
                print "search OPTS  " + _("searching for entry")
                print "tkback OPTS  " + _("take back borrowed file or directory")
                print "update OPTS  " + _("updating files or directories informations")
                print "user OPTS    " + _("user actions")
                print "whereis OPTS " + _("searching for entry and return theirs address")
        
        elif command == "quit" or command == "exit":
            QUIT = True
            
        elif command == "mkcat":
            name = parameters["name"]
            desc = ""
            directory = None
            if parameters.has_key("desc"):
                desc = parameters["desc"]
            if parameters.has_key("dir"):
                directory = parameters["dir"]
            now = datetime.datetime.now()
            infos = {"name":str(name), "description":str(desc),
                     "dateinsert":now, "up_id":0 }
            if parameters.has_key("tags"):
                infos["tags"] = paramaters["tags"]
            EXP.mkDir(address=directory, infos=infos)
                
        elif command == "mkdir":
            now = datetime.datetime.now()
            desc = ""
            name = ""
            directory = None
            infos = {}
            if parameters.has_key("name"):
                name = parameters["name"]
            if parameters.has_key("desc"):
                desc = parameters["desc"]
            
            infos["desc"] = str(desc)
            infos["dateinsert"] = now
            
            if parameters.has_key("tags"):
                infos["tags"] = parameters["tags"]
            if parameters.has_key("dir"):
                directory = parameters["dir"]
                infos["name"] = str(name)
                EXP.mkDir(address=directory, infos=infos)
            elif len(additions)>0:
                name = additions[0]
                infos["name"] = str(name)
                EXP.mkDir(infos=infos)
            
        elif command == "mkfile":
            now = datetime.datetime.now()
            name = ""
            address = None
            infos = {}
            if parameters.has_key("tags"):
                infos["tags"] = str(parameters["tags"])
            if parameters.has_key("type"):
                infos["type"] = str(parameters["type"])
            if parameters.has_key("address"):
                address = parameters["address"]
                infos["name"] = str(name)
                infos["dateinsert"]=now
                EXP.mkFile(infos=infos, address=address)
            elif len(additions)>0:
                name = additions[0]
                infos["name"]=str(name)
                infos["dateinsert"]=now
                EXP.mkFile(infos=infos)
            
        elif command == "ls":
            if parameters.has_key("id"):
                id = parameters["id"]
                EXP.dirList(id=id)
            elif len(additions)>0:
                name = " ".join(additions)
                if name.find("/") != -1:
                    oldId = EXP.dirNow
                    address = EXP.parseAddress(name)
                    for i in address[:-1]:
                        EXP.chDir(dirname=i)
                    EXP.dirList(dirname=address[-1])
                    EXP.dirNow = oldId
                else:
                    EXP.dirList(dirname=name)
            else:
                EXP.dirList()
        
        elif command == "cd":
            if parameters.has_key("id"):
                id = parameters["id"]
                EXP.chDir(id=id)
            elif len(additions)>0:
                name = " ".join(additions)
                if name.find("/") != -1:
                    address = EXP.parseAddress(name)                    
                    for i in address:
                        status = EXP.chDir(dirname=i)
                        if status != True:
                            print _("%s is not a directory"% i)
                else:
                    status = EXP.chDir(dirname=name)
                    if status != True:
                        print _("%s is not a directory"% name)
            
        elif command == "rmdir":
            if parameters.has_key("id"):
                id = parameters["id"]
                EXP.delDir(id=id)
            elif len(additions)>0:
                name = " ".join(additions)
                if name.find("/") != -1:
                    oldId = EXP.dirNow
                    address = EXP.parseAddress(name)
                    for i in address[:-1]:
                        EXP.chDir(dirname=i)
                    EXP.dirDir(dirname=address[-1])
                    EXP.dirNow = oldId
                else:
                    EXP.delDir(dirname = name)
                        
        elif command == "rm":
            if parameters.has_key("id"):
                id = parameters["id"]
                DB.delFile(id=id)
            elif len(additions)>0:
                name = " ".join(additions)
                if name.find("/") != -1:
                    oldId = EXP.dirNow
                    address = EXP.parseAddress(name)
                    for i in address[:-1]:
                        EXP.chDir(dirname=i)
                    EXP.dirFile(filename=address[-1])
                    EXP.dirNow = oldId
                else:
                    EXP.delFile(filename=str(name))
                    
        elif command == "info":
            if len(additions)>0:
                name = " ".join(additions)
                if name.find("/") != -1:
                    oldId = EXP.dirNow
                    address = EXP.parseAddress(name)
                    for i in address[:-1]:
                        EXP.chDir(dirname=i)
                    info = EXP.info(name=address[-1])
                    EXP.dirNow = oldId
                else:
                    info = EXP.info(name=name)
                print info
                
        elif command == "whereis":
            if len(additions)>0:
                wanted = " ".join(additions)
                printList = EXP.search(wanted, "address")
                for i in printList:
                    print i
                    
        elif command == "search":
            if len(additions)>0:
                wanted = " ".join(additions)
                printList = EXP.search(wanted, "all")
                for i in printList:
                    print i
                    
        elif command == "update":
            if len(additions)>0:
                updated = " ".join(additions)
                if updated.find("/") != -1:
                    oldId = EXP.dirNow
                    address = EXP.parseAddress(updated)
                    for i in address[:-1]:
                        EXP.chDir(dirname=i)
                    if len(parameters.keys())>0:
                        EXP.update(updated=address[-1], parameters=parameters)
                    EXP.dirNow = oldId
                elif len(parameters.keys())>0:
                    EXP.update(updated=updated, parameters=parameters)
                    
        elif command == "mv":
            if parameters.has_key("to") and len(additions)>0:
                moved = " ".join(additions)
                to = EXP.parseAddress(parameters["to"])
                params = {}
                
                oldId = EXP.dirNow
                for i in to[:-1]:
                    if i:
                        stat = EXP.chDir(dirname=i)
                        if stat != True:
                            print _("%s is not a directory"% i)
                stat = EXP.chDir(dirname=to[-1])
                if stat != True:
                    params["name"] = to[-1]
                params["up_id"] = EXP.dirNow
                EXP.dirNow = oldId
                
                if moved.find("/") != -1:
                    oldId = EXP.dirNow
                    address = EXP.parseAddress(moved)
                    for i in address[:-1]:
                        EXP.chDir(dirname=i)
                    EXP.update(updated=address[-1], parameters=params)
                    EXP.dirNow = oldId
                else:
                    EXP.update(updated=moved, parameters=params)
                    
        elif command == "cp":
            if parameters.has_key("to") and len(additions)>0:
                copied = " ".join(additions)
                to = EXP.parseAddress(parameters["to"])
                
                EXP.copy(name=copied, to=to)
                
        elif command == "lend":
            if len(additions)>0:
                lended = " ".join(additions)
                if parameters.has_key("to"):
                    uid = parameters["to"]
                else:
                    uid = None
                status = EXP.lend(lended, uid)
                print status[1]
                if status[0] == False:
                    question = None
                    if status[1] == _("That object is borrowed."):
                        question = raw_input(_("Are you want to reserve it? ") +
                                      "(" + _("yes") + "/" + _("no") +"): ")
                    elif status[1] == _("Wait for the order!"):
                        question = raw_input(_("Are you want to reserve it? ") +
                                      "(" + _("yes") + "/" + _("no") +"): ")
                        
                    if question == _("yes"):
                        EXP.reserve(lended, uid)
                    
        elif command == "tkback":
            if len(additions)>0:
                lended = " ".join(additions)
                EXP.takeback(lended)
                
        elif command == "reserve":
            if len(additions)>0:
                reserved = " ".join(additions)
                if parameters.has_key("to"):
                    uid = parameters["to"]
                    EXP.reserve(reserved, uid)
                    
        elif command == "user":
            action = additions[0]
            additions.pop(0)
            if action == "add":
                EXP.addUser(parameters)
            elif action == "del" and len(additions)>0:
                ID = additions[0]
                EXP.delUser(ID)
            elif action == "update" and len(additions)>0:
                ID = additions[0]
                EXP.updateUser(ID, parameters)
            elif action == "info" and len(additions)>0:
                ID = additions[0]
                print EXP.infoUser(ID)
            elif action == "search":
                if len(additions)>0:
                    text = " ".join(additions)
                    EXP.searchUserAll(text)
                else:
                    EXP.searchUserParams(parameters)
                

    print _("Thanks for using bilge-katalog")
    
argv = sys.argv

if "qt" in argv:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
    import mainqt
    
    app = QtGui.QApplication(argv)
    language = QtCore.QLocale.system().name()
    locale = "/usr/share/locale/%s/LC_MESSAGES"% language
    if not os.path.isdir(locale):
        locale = "/usr/share/locale/%s/LC_MESSAGES"% language[:2]
    translator = QtCore.QTranslator()
    translator.load("bilge-katalog.qm", locale)
    app.installTranslator(translator)
    window = mainqt.MainWindow()
    window.show()
    sys.exit(app.exec_())

elif "cli" in argv:
    mainloop()
