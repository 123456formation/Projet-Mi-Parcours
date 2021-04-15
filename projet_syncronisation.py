#from sys import version_info
#from worker import Worker
#from threading import Event
from time import sleep # for test pause
import time  # for test pause
import tkinter as tk
import os
import shutil
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import logging 
import sys
import sys



logging.basicConfig(            # pour avoir des logs qui sont enregistrt sur notre fichier sync.log
    filename='sync.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    )


class pathsync():
    
    def __init__(self):
        self.srcDir = ""
        self.dstDir = ""

    def setsrcDir(self,x):
      
        self.srcDir=x

    def getsrcDir(self):

        return self.srcDir

    def setdstDir(self, y):
        self.dstDir=y
      

    def getdstDir(self):
        
        return self.dstDir



def repertoiredetravail():
    srcDir = str(filedialog.askdirectory(title="Répertoire de travail", initialdir='D:\TEST'))
    #setsrcDir(srcDir)
    print(srcDir)
    path.setsrcDir(srcDir)
    return srcDir


def repertoiredestination():
    dstDir = str(filedialog.askdirectory(title="Répertoire de travail", initialdir='D:\TEST'))
    #setdstDir(dstDir)
    print(dstDir)
    path.setdstDir(dstDir)
    return dstDir


def syncDirs():
    rootDir1= path.getsrcDir()
    rootDir2= path.getdstDir()
    print(rootDir1)
    print(rootDir2)
    logging.info('La syncro démarre')
    print("sono dans la methode")
    for root1, dirs1, files1 in os.walk(rootDir1):
        for relativePath1 in dirs1 :
            fullPath1 = os.path.join(root1, relativePath1)
            fullPath2 = fullPath1.replace(rootDir1, rootDir2)
            if os.path.exists(fullPath2) and os.path.isdir(fullPath2) :
                continue
            if os.path.exists(fullPath2) and os.path.isfile(fullPath2) :
                raise Exception("Cannot perform dir sync." + str(fullPath2) + " should be a dir, not a file!")
                logging.ERROR("Cannot perform dir sync." + str(fullPath2) + " should be a dir, not a file!")
            # Case 1 : dest dir does not exit
            shutil.copytree(fullPath1, fullPath2)
            print("Directory " + str(fullPath2) + " copied from " + str(fullPath1))
            logging.INFO("Directory " + str(fullPath2) + " copied from " + str(fullPath1))
            continue
    for root2, dirs2, files2 in os.walk(rootDir2):
        for relativePath2 in dirs2:
            fullPath2 = os.path.join(root2, relativePath2)
            fullPath1 = fullPath2.replace(rootDir2, rootDir1)
            if os.path.exists(fullPath1) and os.path.isdir(fullPath1) :
                continue
            if os.path.exists(fullPath1) and os.path.isfile(fullPath1) :
                raise Exception("Cannot perform dir sync." + str(fullPath1) + " should be a dir, not a file!")
                logging.error(("Cannot perform dir sync." + str(fullPath1) + " should be a dir, not a file!"))
            # Case 3 : dest dir exists but not src dir, so we need to copy it
            shutil.copytree(fullPath2, fullPath1)
            print("Directory " + str(fullPath1) + " copied from" + str(fullPath2))
            logging.INFO("Directory " + str(fullPath1) + " copied from" + str(fullPath2))
            continue
    syncFiles()


def syncFiles():
    #thread.start()
    print("je suis dans  syc file")   # juste pour veridier que ma mathode elle marche
    rootDir1= path.getsrcDir()
    rootDir2= path.getdstDir()
    print(rootDir1)     # pour verifier 
    print(rootDir2)    #pour verifier 
    
    
    for root1, dirs1, files1 in os.walk(rootDir1):
        time.sleep (x)
        for file1 in files1:
            time.sleep (x)
            fullPath1 = os.path.join(root1, file1)
            fullPath2 = fullPath1.replace(rootDir1, rootDir2)
            # Case 1 : le file n'existe pas  in dest dir
            if (not os.path.exists(fullPath2)) :
                time.sleep (x)
                shutil.copy2(fullPath1, fullPath2)
                print("File " + str(fullPath2) + " copied from " + str(fullPath1))
                logging.info(("File " + str(fullPath2) + " copied from " + str(fullPath1)))
                continue
            # Case 2 : src file est plus recent  que  dest file
            file1LastModificationTime = round(os.path.getmtime(fullPath1))
            file2LastModificationTime = round(os.path.getmtime(fullPath2))
            if (file1LastModificationTime > file2LastModificationTime):
                time.sleep (x)
                os.remove(fullPath2)
                shutil.copy2(fullPath1, fullPath2)
                print("File " + str(fullPath2) + " synchronized from " + str(fullPath1))
                logging.info("File " + str(fullPath2) + " synchronized from " + str(fullPath1))
                continue
            # Cas 3 : dest file est plus recent que le src file 
            if (file1LastModificationTime < file2LastModificationTime):
                time.sleep (x)
                os.remove(fullPath1)
                shutil.copy2(fullPath2, fullPath1)
                print("File " + str(fullPath1) + " synchronized from " + str(fullPath2))
                logging.info("File " + str(fullPath1) + " synchronized from " + str(fullPath2))
                continue
    # Cas 4 : file exist seuelemnt in dest dir mais non in  src , donc on va le copier dans la src dir

    for root2, dirs2, files2 in os.walk(rootDir2):
        time.sleep (x)
        for file2 in files2:
            sleep (x)
            fullPath2 = os.path.join(root2, file2);
            fullPath1 = fullPath2.replace(rootDir2, rootDir1);
            if (os.path.exists(fullPath1)):
                continue
            shutil.copy2(fullPath2, fullPath1)
            print("File " + str(fullPath1) + " copied from " + str(fullPath2))
            logging.info("File " + str(fullPath1) + " copied from " + str(fullPath2))



def pause() :       # fonction pause qui n'a pas marché à voir avec leila 
    exit.set()
   
x=0

exit = Event()
x=0
path=pathsync()

app = tk.Tk()

srcButton = tk.Button(app, text="Répertoire de travail",command=repertoiredetravail)
dstButton = tk.Button(app, text="Fichier Destination",command=repertoiredestination)
syncButton= tk.Button(app, text="Sync1", command=syncDirs, bg='#54FA9B')
quitButton=tk.Button(app, bg='#54FA9B', text="Quit",  command=app.destroy).pack() 
pauseButton=tk.Button(app, bg='#54FA9B',text="Pause", command=pause).pack()
app.configure(bg='yellow')
app.geometry('300x300')
app.title("Application Syncronisation Dossier" )
#thread = Worker(syncFiles) 

srcButton.pack()
dstButton.pack()
syncButton.pack()

app.mainloop()