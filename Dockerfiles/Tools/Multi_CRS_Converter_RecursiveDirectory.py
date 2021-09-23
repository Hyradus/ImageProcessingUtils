#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Multi CRS repojector
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
## **Multiple-format CRS Converter**

This notebook convert any CRS, if present, of all files with specific extension in a user-selected folder into user-selected CRS.
- **If crs of source file is not availabe, the file will be copied in "Missing crs folder"
- **If source file is empty it will be copied in "Empty files folder"

- **All file with extension different from [shp/SHP, tiff/TIFF, tif/tif, gpkg/GPKG] will be ignored**
- **At the moment is not recursive**
### **TO-DO**
- [x] Add recursive search
- [x] Add a function to move all not supported files in the destination path, recustructing the original strucutre of the directories

For problems contact: g.nodjoumi@jacobs-university.de


Created on Thu Nov 19 21:14:11 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
from argparse import ArgumentParser
from tkinter import Tk,filedialog
import os
from tqdm import tqdm
from GenUtils import get_paths, make_folder
from ReprojUtils import converter
    

def dir_conv(folder):
    
    dst_path = folder.replace(DATA_PATH, WORK_PATH)

    try:
        make_folder(dst_path, None)
    except:
        import time
        while True:
            try:
                make_folder(dst_path, None)
            except:
                # print('error', dst_path)
                time.sleep(10)
            else:
                continue
    
    all_files= get_paths(folder, '*')
    extensions = set()
    for file in all_files:
        pathname, exten = os.path.splitext(file)
        if exten.split('.')[1] in ['tiff','tif','gpkg','shp']:
            extensions.add(exten)
        
            
    for exts in extensions:
        exts=exts.split('.')[1]
        make_folder(dst_path, exts)
        
    for file in all_files:
        converter(file, dst_path, folder, OUT_CRS)
    return(len(all_files))

def main():        
    # List all files
    folder_list = [x[0] for x in os.walk(DATA_PATH)]        

    with tqdm(total=len(folder_list),
              desc = 'Generating files',
              unit='File') as pbar:
        
        for i in range(len(folder_list)):
                dir_conv(folder_list[i])
                              
                pbar.update(1)

if __name__ == "__main__":

    parser = ArgumentParser()
    
    parser.add_argument('--wdir', help='Output folder: ')
    parser.add_argument('--ddir', help='Input files folder: ')
    parser.add_argument('--crs', help='Output CRS')
        
    args = parser.parse_args()
    WORK_PATH = args.wdir
    DATA_PATH = args.ddir
    OUT_CRS = args.crs

    ## PATHS
    #WORK_PATH = '/media/gnodj/W-DATS/Projects/ANALOG-1-Miracles/WGS84_UTM33N_2'
    if WORK_PATH is None:
        root = Tk()
        root.withdraw()
        WORK_PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Select output folder")
        print('Output folder:', WORK_PATH)

    
    #DATA_PATH = '/media/gnodj/W-DATS/Projects/ANALOG-1-Miracles/0_planning_gis_v01_CHECK-DATUMS_CRS'
    # DATA_PATH = '/media/gnodj/W-DATS/Projects/ANALOG-1-Miracles/0_planning_gis_v01_CHECK-DATUMS_CRS/background_gis/data_from_ingv'
    if DATA_PATH is None:
        root = Tk()
        root.withdraw()
        DATA_PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Select input files folder")
        print('Input files folder:', DATA_PATH)
    
       
    OUT_CRS = '+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs'
    if OUT_CRS is None:
        OUT_CRS = input('Type destination CRS string')
   
    main()    




