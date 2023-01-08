import os
import csv
import shutil

pathinput =r"D:\Moana\Data\Galaxies\M77"
trashpath=r"D:\Moana\Data\Trash"

#___________________________________________________________________________________________________________________________
#___________________________________________________________________________________________________________________________
def removebadframes(pathinput):
    csvfilename=os.path.join(pathinput,"a.csv")
    with open(csvfilename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if row[0].isnumeric():
                approval=str(row[1])
                fitfile=str(row[3]) # there is a bug in Pixinsight, gives linux paths rather than OS dependant paths
                fwhm=float(row[13])
                eccentricity=float(row[14])
                #print(', '.join(row))
                if approval=="false":# or eccentricity>0.508 or fwhm>7.0:
                    (root,file)=os.path.split(fitfile.strip('\"'))
                    badfile=os.path.join(trashpath,file)
                    original=os.path.join(pathinput,file)
                    print ("Move ",original," to ",badfile,"---", approval,fwhm,eccentricity)
                    shutil.move(original,badfile)
        
removebadframes(pathinput)