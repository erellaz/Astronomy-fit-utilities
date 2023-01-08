# -*- coding: utf-8 -*-
import os
from astropy.io import fits
import zipfile

pathinput =r"D:\Moana\Data\Nebulas\S279_Running_Man\\"

#____________________________________________________________________________________________________
# Change the lat long in fit file, or change any other header
def change_fit_header(fits_file):
    print("Sanitizing: ",fits_file)
    with fits.open(fits_file, mode='update') as hdul:
        # Sanitize observatory coordinates.
        hdr = hdul[0].header
        hdr['OBSERVER'] = ('GSR the Remote Telescope Pilot', 'Observer name')
        hdr['SITELAT'] = ('30 34 00.000', 'Approx latitude of the imaging site degrees')
        hdr['SITELONG'] = ('-104 5 00.000', 'Approx longitude of the imaging site degrees')

        #make filter names consitent between various acquistion software
        if (hdr['FILTER']==('R')):
            hdr['FILTER']==('Red  ')
            print("Fixing Red")
        if (hdr['FILTER']==('G')):
            hdr['FILTER']==('Green  ')
            print("Fixing Green")
        if (hdr['FILTER']==('B')):
            hdr['FILTER']==('Blue  ')
            print("Fixing Blue")
            
        hdul.flush()  # changes are written back to original.fits
#____________________________________________________________________________________________________  
# Iterate for every fit in the directory
def sanitizeall(pathinput):
    dirsinput = os.listdir( pathinput )
    for item in dirsinput:
        split_item = os.path.splitext(item)
        if os.path.isfile(pathinput+item) and (split_item[1]==".fit" or split_item[1]==".fits"):
            change_fit_header(os.path.join(pathinput,item))
            

#____________________________________________________________________________________________________
def compress(pathinput):
    dirsinput = os.listdir( pathinput )
    print("Compressing content of:", pathinput)

    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile(os.path.join(pathinput,"RAWs.zip"), mode="w")
    try:
        for item in dirsinput:
            split_item = os.path.splitext(item)
            if os.path.isfile(pathinput+item) and (split_item[1]==".fit" or split_item[1]==".fits"):
                # Add file to the zip file
                # first parameter file to zip, second filename in zip
                print("Now compressing file:", item)
                zf.write(os.path.join(pathinput,item), item, compress_type=compression)

    except FileNotFoundError:
        print("An error occurred")
    finally:
        # Don't forget to close the file!
        zf.close()
        print("Done - Compression complete!")

#____________________________________________________________________________________________________            
sanitizeall(pathinput)
compress(pathinput)