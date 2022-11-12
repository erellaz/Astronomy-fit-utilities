# -*- coding: utf-8 -*-
import os
from astropy.io import fits

pathinput =r"D:\Moana\Data\Trash\\"


#____________________________________________________________________________________________________
# Change the lat long in fit file, or change any other header
def change_fit_header(fits_file):
    with fits.open(fits_file, mode='update') as hdul:
        # Change something in hdul.
        hdr = hdul[0].header
        hdr['OBSERVER'] = ('GSR the Remote Telescope Pilot', 'Observer name')
        hdr['SITELAT'] = ('30 34 00.000', 'Approx latitude of the imaging site degrees')
        hdr['SITELONG'] = ('-104 5 00.000', 'Approx longitude of the imaging site degrees')
        hdul.flush()  # changes are written back to original.fits
#____________________________________________________________________________________________________  
# Iterate for every fit in the directory
def sanitizeall(pathinput):
    dirsinput = os.listdir( pathinput )
    for item in dirsinput:
        split_item = os.path.splitext(item)
        if os.path.isfile(pathinput+item) and split_item[1]==".fit":
            change_fit_header(os.path.join(pathinput,item))
            
#____________________________________________________________________________________________________            
sanitizeall(pathinput)