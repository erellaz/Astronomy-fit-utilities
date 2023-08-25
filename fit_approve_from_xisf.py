import os
import shutil

fitsourcedir=r"G:\Moana\Stage"
xisfsourcedir=r"G:\Moana\Stage\Sh2 101 approved"
targetdir=r"G:\Moana\Data\temp\Tulip"


for xdirpath, xdirs, xfiles in os.walk(xisfsourcedir):	
    for xfilename in xfiles:
        xfname = os.path.join(xdirpath,xfilename)
        xffilename=xfilename[:-7]+".fits"
        #print(xfilename, xffilename)
        
        for fdirpath, fdirs, ffiles in os.walk(fitsourcedir):
            for ffilename in ffiles:
                if xffilename == ffilename:
                    #print(xffilename," matches ", ffilename)
                    msource = os.path.join(fdirpath,ffilename)
                    mtarget = os.path.join(targetdir,ffilename)
                    shutil.move(msource,mtarget)
                    #print("mv ",msource,mtarget)