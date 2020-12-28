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
import pathlib

from argparse import ArgumentParser
from tkinter import Tk,filedialog
from rasterio.enums import Resampling
import rasterio as rio

import cv2 as cv

from TileFuncs import Dim2Tile, TileNumCheck
from GenUtils import question, make_folder, get_paths, intInput, chunk_creator
from ImgUtils import ImgWriter
global PATH
global dim
global ext
global rasters
global folder

def slicer(image, width, height, image_name, mode, dim):
    from rasterio.windows import Window
    import math
    
    if mode in ['D', 'd']:
       
       vt=Dim2Tile(dim, width)
       vt = TileNumCheck(vt, width, dim)
       ht = Dim2Tile(dim, height)
       ht = TileNumCheck(ht, height, dim)
	    
    else:
        if width > height:
            vt = tiles
            ht = math.ceil(tiles/2)
            
        else:
            vt = math.ceil(tiles/2)
            ht = tiles
    print('Generationg: ', vt*ht ,' tiles')
    for ih in range(ht):
        for iw in range(vt):
            save_name = folder+'/'+image_name+'_H'+str(ih)+'_V'+str(iw)+'.'+ext
            
            
            x = math.floor(width/vt*iw)
      
            y = math.floor(height/ht*ih)
            h = math.floor(height/ht)
            w = math.floor(width/vt)
            if dim is None:
                dim = math.floor(height/ht)

            win = Window(x,y,w,h)
  
            tile_transform = image.window_transform(win)
            img = image.read(1, window=win)
            img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
            # img = cv.convertScaleAbs(img, alpha=(255.0/img.max()))
            ImgWriter(save_name, img, image.crs, tile_transform, ext)
            

def JP2PNGW(file):
    image_name= pathlib.Path(file).name.split('.')[0]
    image = rio.open(file)
    
    width = image.width
    height = image.height

    if sli in ['Y', 'y']:
        slicer(image, width, height, image_name, mode, dim)
 
    else:
        new_height=dim
        new_width = int(width*new_height/height)
    
  
        
    
        img = image.read(
                    out_shape=(image.count, new_height, new_width),
                    resampling=Resampling.nearest,
                )
        
        transform = image.transform * image.transform.scale(
                    (image.width / img.shape[-1]),
                    (image.height / img.shape[-2]))
    
        # t = transform
        # params = [t.a,t.b,t.d,t.e,t.c,t.f]
        
        
        img = cv.convertScaleAbs(img, alpha=(255.0/img.max()))[0]
        
    
        
        save_name=folder+'/'+image_name+'.'+ext

        ImgWriter(save_name, img, image.crs, transform, ext)



def parallel_JP2PNG(files, JOBS):
    from joblib import Parallel, delayed
    
    Parallel (n_jobs=JOBS)(delayed(JP2PNGW)(files[i])
                           for i in range(len(files)))
 
def main():

    from tqdm import tqdm
    import psutil
    avram=psutil.virtual_memory().total >> 30
    if dim is None:
        JOBS=psutil.cpu_count(logical=False)        
    elif avram > 30 and dim <=8192:
        JOBS=psutil.cpu_count(logical=False)
    elif avram >30 and dim>8192:
        JOBS=psutil.cpu_count(logical=False)
    elif avram <30 and dim <=8192:
        JOBS=psutil.cpu_count(logical=False)
    elif avram <30 and dim >8192:
        JOBS=2
        
    print('\nToral ram: ', avram, ' , using: ', JOBS, ' cpus')
    rasters = get_paths(PATH, 'jp2')
    
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
    parser.add_argument('--sli', help='Slice images?')
    parser.add_argument('--mode', help='Slice by dimension or tile number (D/d or T/t')
    parser.add_argument('--t', help='Specify total number of tiles')
    parser.add_argument('--dim', help='Desired height or width of the tiles')
    
    parser.add_argument('--ext', help='output file format (tiff,png,jpg')
    args = parser.parse_args()  

    PATH = args.PATH
    sli = args.sli
    
    ext=args.ext
    mode=args.mode
    tiles = args.t
    dim = args.dim
    
    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Please select the folder with JP2 files")
        print('Working folder:', PATH)

    if sli is None:
        sli = question('Slice images?\n', ['Y','y','N','n'])
     
    if sli in ['Y', 'y']:
        
        if mode is None:
                while mode not in ['D','d','T','t']:  
                    mode = question('Select mode for slicing:\nD/d slice by tile dimension\nT/t slice by tile number\n',['D','d','T','t'])
                    
        if mode in ['T','t']:
            if tiles is None:
                tiles = intInput('number of tiles')
                folder_name='Tiled_'+str(tiles)+'Tiles'
        elif mode in ['D', 'd']:
            if dim is None:
                dim= intInput('tile desired width or height')
                folder_name='Tiled_'+str(dim)+'px'
    
    else:
    
        while True:
            try:
                dim = int(input('Insert desired vertical resolution in pixels: to resize images ' ))
            except:
                print('Please insert only integer')
                # continue
            if isinstance(dim, int):
                break
            
    if ext is None:
        while ext not in ['TIFF','tiff','PNG','png','JPG','jpg']:
            print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
            ext = input('Enter output format: ')
                
        
    # os.chdir(PATH)
    
    # folder = make_folder(ext)
    folder = make_folder(PATH, ext)
    
    main()



