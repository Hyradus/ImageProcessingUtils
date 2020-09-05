#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: JP2 to TIFF/PNG/JPG converter + TFW/PGW/JGW
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de

This script use pyqgis to load JP2 images and convert into tiff/png/jpg of a given resolution,
saving also a world reference file.

Compatible with Tiff, PNG, JPG

Created on Wed Aug  5 18:47:33 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""


import os
import shutil
from datetime import datetime
import pathlib

from argparse import ArgumentParser
from tkinter import Tk,filedialog

import rasterio as rio
from rasterio.enums import Resampling
import cv2 as cv



global PATH
global vres
global ext

def answer(question):
    answ = None
    while answ not in ['yes','y','no','n']:
        print("Please enter yes/y or no/n.")    
        answ = input(question+': ')
    return(answ)

def make_folder(name):
    os.getcwd()
    folder = name
    if os.path.exists(folder):
           qst = name + ' Folder exist, remove it? '
           answ = answer(qst)
           if answ in ['yes', 'y']:               
               shutil.rmtree(folder)
               os.mkdir(folder)
               print(name, 'Folder created')
           else:
               now = datetime.now()
               new_name = name +'_' + now.strftime("%d-%m-%Y_%H-%M-%S")
               print(new_name, ' Folder not exist, creating.')
               os.mkdir(new_name)
               print('Created new ', name,' Folder')
    else:
        print(name, ' Folder not exist, creating.')
        os.mkdir(folder)
        print('Created new ', name,' Folder')
    return(folder)

def get_paths(PATH):
    # from pathlib import Path

    # for path in Path(PATH).rglob('*.JP2'):
    #     print(path.name)
    import glob
    os.chdir(PATH)
    filename = [i for i in glob.glob('**/*.JP2',recursive=True)]
    return(filename)




def JP2PNGW(file):
    image_name= pathlib.Path(file).name.split('.')[0]
    image = rio.open(file)
    # max_height = vres
    width = image.width
    height = image.height
    
 
    new_height=vres
    new_width = int(width*new_height/height)
    
    # profile = image.profile
    
    
    data = image.read( # Note changed order of indexes, arrays are band, row, col order not row, col, band
                out_shape=(image.count, new_height, new_width),
                resampling=Resampling.cubic,
            )
    
    transform = image.transform * image.transform.scale(
                (image.width / data.shape[-1]),
                (image.height / data.shape[-2]))

    img = cv.convertScaleAbs(data, alpha=(255.0/data.max()))[0]
    name=PATH+'/'+fname+'/'+image_name+'_uint8'
    cv.imwrite(name+'.'+ext,img)
    t = transform
    
    params = [t.a,t.b,t.d,t.e,t.c,t.f]
    if ext == 'tiff':
        wfext='.tfw'
    elif ext == 'png':
        wfext='.pgw'
    elif ext == 'jpg':
        wfext='.jgw'
    with open(name+wfext, "w") as output:
        for row in params:
            output.write(str(row)+'\n')



def parallel_JP2PNG(files, JOBS):
    from joblib import Parallel, delayed
    
    Parallel (n_jobs=JOBS)(delayed(JP2PNGW)(files[i])
                           for i in range(len(files)))
 

def chunk_creator(item_list, chunksize):
    import itertools

    it = iter(item_list)
    while True:
        chunk = tuple(itertools.islice(it, chunksize))
        if not chunk:
            break
        yield chunk



def main():

    from tqdm import tqdm
    import psutil
    avram=psutil.virtual_memory().total >> 30
    
    if avram > 30 and vres <=8192:
        JOBS=psutil.cpu_count(logical=True)
    elif avram >30 and vres>8192:
        JOBS=psutil.cpu_count(logical=False)
    elif avram <30 and vres <=8192:
        JOBS=psutil.cpu_count(logical=False)
    elif avram <30 and vres >8192:
        JOBS=2
    
    print('\nToral ram: ', avram, ' , using: ', JOBS, ' cpus')
    rasters = get_paths(PATH)
    with tqdm(total=len(rasters),
             desc = 'Generating images and world files',
             unit='File') as pbar:
        
        filerange = len(rasters)
        chunksize = round(filerange/JOBS)
        if chunksize <1:
            chunksize=1
            JOBS = filerange
        chunks = []
        for c in chunk_creator(rasters, JOBS):
            chunks.append(c)
            
    
        for i in range(len(chunks)):
            files = chunks[i]    
            print('\nConverting: ', files)
            parallel_JP2PNG(files, JOBS)
            pbar.update(JOBS)
            

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--PATH', help='Directory with JP2 files')
    parser.add_argument('--vres', help='Max vertical resolution')
    parser.add_argument('--ext', help='output file format (tiff,png,jpg')
    args = parser.parse_args()  

    PATH = args.PATH
    vres = args.vres
    ext=args.ext
    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Please select the folder with JP2 files")
        print('Working folder:', PATH)
    
    if vres is None:
        while True:
            try:
                vres = int(input('Insert max vertical resolution in pixels: to resize images ' ))
            except:
                print('Please insert only integer')
                # continue
            if isinstance(vres, int):
                break
    if ext is None:
        while ext not in ['TIFF','tiff','PNG','png','JPG','jpg']:
            print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
            ext = input('Enter output format: ')
        
    os.chdir(PATH)
    rasters = get_paths(PATH)
    fname = make_folder(ext)

    
    main()


