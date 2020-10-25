#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Multi Image Parallel Slicer 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de

This script simply divide all images of a folder in a number of vertical and
horizontal tiles provided by user.

It also attempt, if requested by user, to adapt vertical and horizontal tiles 
number to return tiles with almost 1:1 aspect ratio. (TO BE imrpooved)

Created on Tue Aug 11 18:46:42 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""

import os

from PIL import Image
Image.MAX_IMAGE_PIXELS = None

import pathlib
from argparse import ArgumentParser
from tkinter import Tk,filedialog
from tqdm import tqdm
import psutil

from TileFuncs import Dim2Tile, TileCheckSave, TileNumCheck
from utils import question, make_folder, get_paths, intInput, chunk_creator

global PATH
global image_list
global folder
global tiles
global dimension
global ixt
global oxt
global mode


def slicer(image):    
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(image)
    
    width, height = img.size
    
    if height >=900 and width > 900:
        image_name= folder+'/'+pathlib.Path(image).name.split('.')[0]
        
        if mode in ['D', 'd']:
            
            vt=Dim2Tile(dim, width)
            vt = TileNumCheck(vt, width, dim)
            ht = Dim2Tile(dim, height)
            ht = TileNumCheck(ht, height, dim)
	    
        else:
            vt = tiles
            ht = tiles
            
        for ih in range(ht):
            for iw in range(vt):
                save_name = image_name+'_H'+str(ih)+'_V'+str(iw)+'_.'+oxt
                TileCheckSave(img, save_name, vt, ht, iw, ih)
                
def parallel_slicer(files, JOBS):
    from joblib import Parallel, delayed
    Parallel (n_jobs=JOBS)(delayed(slicer)(files[i])
                            for i in range(len(files)))

def main():
    JOBS=psutil.cpu_count(logical=True)
    
    with tqdm(total=len(image_list),
             desc = 'Generating Images',
             unit='File') as pbar:
        
        filerange = len(image_list)
        chunksize = round(filerange/JOBS)
        if chunksize <1:
            chunksize=1
            JOBS = filerange
        chunks = []
        for c in chunk_creator(image_list, JOBS):
            chunks.append(c)
        
        
        for i in range(len(chunks)):
            files = chunks[i]
            print('\nSlicing: ', files)
            parallel_slicer(files, JOBS)
            pbar.update(JOBS)



if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--PATH', help='Directory with the files to be tiled')
    parser.add_argument('--mode', help='Slice by dimension or tile number (D/d or T/t')
    parser.add_argument('--t', help='Specify total number of tiles')
    parser.add_argument('--dim', help='Desired height or width of the tiles')
    parser.add_argument('--ixt', help='input file format (tiff,png,jpg')
    parser.add_argument('--oxt', help='output file format (tiff,png,jpg')

    
    args = parser.parse_args()  
    PATH = args.PATH
    mode=args.mode
    tiles = args.t
    dim = args.dim
    ixt = args.ixt
    oxt = args.oxt
    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,title="Please select the folder with the files to be tiled")
        print('Working folder:', PATH)
    
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
    
    if ixt is None:
        while ixt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
            print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
            ixt = input('Enter input image format: ')
    
    if oxt is None:
        while oxt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
             print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
             oxt = input('Enter output image format: ')
    # os.chdir(PATH)
    
    folder = make_folder(PATH, folder_name)
    image_list = get_paths(PATH, 'png') #edit image file extension
    
    main()
