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

# import image_slicer as ims
import os 
from datetime import datetime
import shutil
# from PIL import Image
import cv2 as cv
import pathlib
from argparse import ArgumentParser
from tkinter import Tk,filedialog

global PATH
global image_list
global folder
global vtiles
global htiles

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
               folder = name +'_' + now.strftime("%d-%m-%Y_%H-%M-%S")
               print(folder, ' Folder not exist, creating.')
               os.mkdir(folder)
               print('Created new ', name,' Folder')
    else:
        print(name, ' Folder not exist, creating.')
        os.mkdir(folder)
        print('Created new ', name,' Folder')
    return(folder)

def get_paths(PATH, ext):
    import glob
    os.chdir(PATH)
    filename = [i for i in glob.glob('**/*.'+ext,recursive=True)]
    return(filename)


# def slicer(image):
#     print('\nSlicing: ', image, ' in ', tiles, ' tiles.')
#     Image.MAX_IMAGE_PIXELS = None
#     # height = cv.imread(image).shape[0]
#     # if height > 2048:
#     ims.slice(image, tiles)
#     shutil.move(image, folder)

def slicer(image, answ):    
    img = cv.imread(image)    
    height, width, channels = img.shape
    vt = vtiles
    ht = htiles
    if answ in ['yes', 'y']:
        asp_ratio = round(width/height, 1)
        if asp_ratio < 1.1 and asp_ratio > 0.9:
            vt = 2
            ht = 2
        elif asp_ratio <= 0.9 and asp_ratio > 0.4:
            max_height = int(height*asp_ratio)
            ht = int(height/max_height)*2
        elif asp_ratio <=0.4:
            max_height = int(height*asp_ratio)
            ht = int(height/max_height)+1
        elif asp_ratio >=1.1 and asp_ratio <2:
            vt = 2
            ht =1
        elif asp_ratio >=2:
            vt= int(asp_ratio)
            ht=1
        
    # elif asp_ratio <=0.3:
    #     max_height = int(height*asp_ratio)
    #     ht = int(height/max_height)
    # elif asp_ratio > 1:
    #     vt = 1
    #     ht = ht/2
        
    for ih in range(ht):
        for iw in range(vt):
    
            x = int(width/vt*iw)
            y = int(height/ht*ih)
            h = int((height/ht))
            w = int((width/vt))
            print(x,y,h,w)
            tile = img[y:y+h, x:x+w]

            image_name= folder+'/'+pathlib.Path(image).name.split('.')[0]+'_H'+str(ih)+'_V'+str(iw)+'_.png'
            cv.imwrite(image_name,tile)
          
        
def parallel_slicer(files, JOBS, answ):
    from joblib import Parallel, delayed
    Parallel (n_jobs=JOBS)(delayed(slicer)(files[i], answ)
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
    JOBS=psutil.cpu_count(logical=True)
    # JOBS = 2
    
    with tqdm(total=len(image_list),
             desc = 'Generating PNGs',
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
            print('\nRendering: ', files)
            parallel_slicer(files, JOBS, ratio_answ)
            pbar.update(JOBS)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--PATH', help='Directory with the files to be tiled')
    parser.add_argument('--vt', help='Specify vertical tiles')
    parser.add_argument('--ht', help='Specify horizontal tiles')
    parser.add_argument('--art', help='Try to maintain 1:1 aspect ratio (Y/y or N/n')
    
    args = parser.parse_args()  
    PATH = args.PATH
    vtiles = args.vt
    htiles = args.ht
    ratio_answ = args.art

    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Please select the folder with the files to be tiled")
        print('Working folder:', PATH)
    if vtiles is None:
        while True:
            try:
                vtiles = int(input('Insert number of vertical tiles: ' ))
            except:
                print('Please insert only one integer')
                # continue
            if isinstance(vtiles, int):
                break
    if vtiles is None:
        while True:
            try:
                htiles = int(input('Insert number of horizontal tiles: ' ))
            except:
                print('Please insert only one integer')
                # continue
            if isinstance(htiles, int):
                break
    if ratio_answ is None:
        ratio_answ=answer('\nTry to mantain 1:1 aspect ratio? ')

    os.chdir(PATH)

    image_list = get_paths(PATH, 'png') #edit image file extension

    folder_name='Tiled_H'+str(htiles) +'_V'+str(vtiles)
    folder = make_folder(folder_name)

    
    main()