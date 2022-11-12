# -*- coding: utf-8 -*-
# Import daily astronomy image production, select, rename 
# and dispatch to final folder destination

import os
import shutil
import re
import csv

pathinput =r"D:\Moana\Stage\Light\\"
pathoutput =r"D:\Moana\Data\\"
pathtoscan =r"D:\Moana\Data\\"
trashpath=r"D:\Moana\Data\Trash\\"
namepattern="_60"

#___________________________________________________________________________________________________________________________
#___________________________________________________________________________________________________________________________
#___________________________________________________________________________________________________________________________
# Opens the .csv output of the PixInsight Frame Selector script
# Use the info in the .csv to select the good frames
def removebadframes(pathinput,trashpath):
    csvfilename=os.path.join(pathinput,"a.csv")
    with open(csvfilename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if row[0].isnumeric():
                approval=row[1]
                fitfile=str(row[3])
                fitfile=fitfile.replace("\"","")
                fwhm=float(row[13])
                eccentricity=float(row[14])
                #print(', '.join(row))
                print("Considering file: ",fitfile, approval,fwhm,eccentricity)
                if approval=="false" or eccentricity>0.65 or fwhm>4:
                    (root,file)=os.path.split(fitfile)
                    badname=os.path.join(trashpath,file)
                    print ("This file needs to be moved ",fitfile," to ",badname,"---", approval,fwhm,eccentricity)
                    try:
                        shutil.move(fitfile,badname)
                    except:
                        print(fitfile," not found!")
#_______________________________________________________________________________________________________________________
# Rename fit files to avoid name collisions
def renamesgp(pathinput,namepattern):
    dirsinput = os.listdir( pathinput )
    for item in dirsinput:
        split_item = os.path.splitext(item)
        if os.path.isfile(os.path.join(pathinput,item)) and split_item[1]==".fit":
            newname=item.replace("_00",namepattern)
            print("Renaming",item,newname)
            os.rename(os.path.join(pathinput,item),os.path.join(pathinput,newname)) 

#___________________________________________________________________________________________________________________________  
# Move each fit file to the directory matching the object name
def movetostorage(pathinput,pathoutput):
    dirsinput = os.listdir( pathinput )
    dirsoutput = os.listdir( pathoutput )
    for item in dirsinput:
        split_item = os.path.splitext(item)
        if os.path.isfile(pathinput+item) and split_item[1]==".fit":
            astrotarget=item.split('_')
            print("Identified astro object",astrotarget[0]," for picture ",item)
            #Agressive reduction of the input image name for better matching
            mi=astrotarget[0].casefold()
            mi=mi.replace(' ','')
            mi=mi.replace('-','')
            mi=mi.replace('_','')
            
            for t in dirsoutput:
                 moo=t.split('_')   
                 mo=moo[0].casefold()
                 mo=mo.replace(' ','')
                 mo=mo.replace('-','')
                 mo=mo.replace('_','')
                 if mo == mi:
                     #print("    Matched ",mi, mo, " performing copy of", item, " to ", t)
                     print("    Matched picture:", item, " to diectory ", t)
                     isource=os.path.join(pathinput,item)
                     idest=os.path.join(pathoutput,t)
                     print("move ",isource,idest)
                     try:
                         shutil.move(isource,idest)
                     except:
                         "Moving failed"
#___________________________________________________________________________________________________________________________
# For each target, make a sensus of the various kind of frame, to help with the next program
def scan_dir(pathtoscan):
    # walk the directory
    for root, subdir, files in os.walk(pathtoscan):
       (Ha,OIII,SII,red,green,blue,lum)=(0,0,0,0,0,0,0)
       print(os.path.basename(root),"------>", len(files))
       for file in files:
           #print(file)
           if re.search("Ha",file):
               Ha=Ha+1
           if re.search("OIII",file):
               OIII=OIII+1
           if re.search("SII",file):
               SII=SII+1
           if re.search("red",file):
               red=red+1
           if re.search("green",file):
               green=green+1
           if re.search("blue",file):
               blue=blue+1
           if re.search("lum",file):
               lum=lum+1
       print("Ha=",Ha,"  OIII=",OIII,"  SII=",SII,"  Red=",red,"  Green=",green,"  Blue=",blue,"  Lum=",lum,"\n")
   
#___________________________________________________________________________________________________________________________                   
# remove the bad frames detected by Pixinsight
removebadframes(pathinput,trashpath)

# Rename to avoid name collisions
renamesgp(pathinput,namepattern)

# Move
movetostorage(pathinput,pathoutput)

# Count what we have
scan_dir(pathtoscan)