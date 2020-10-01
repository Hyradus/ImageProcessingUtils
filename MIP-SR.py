#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Multi Image Parallel Square Resizer
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de

This script resize with center cut images to a 1:1 ratio.

If requested by user, it also resize all images to 900x900 pixels


Created on Tue Aug 11 18:46:42 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""


import os 
from datetime import datetime
import shutil
from PIL import Image
import cv2 as cv
import pathlib
from tkinter import Tk,filedialog
from argparse import ArgumentParser

global PATH
global folder
global res
global ixt
global oxt

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
    filename = [i for i in glob.glob('**/*.'+ixt,recursive=True)]
    return(filename)




def cropper(image):
    
    from PIL import ImageOps
    img = Image.open(image)
    size = (1024,1024)
    img = ImageOps.fit(img, size, Image.ANTIALIAS)
    image_name= folder+'/'+pathlib.Path(image).name.split('.')[0]+'_cropped.'+oxt
    img.save(image_name)
    
def square_crop(image):
    img = cv.imread(image)
    height = img.shape[1]
    width = img.shape[0]
    
    center_x = width//2
    center_y = height//2
    diff = abs(width-height)
    
    if width < height:
        print('a')
        x= width
        y=height-diff
        w = diff//2
        h = 0
    elif width > height:
        print('b')
        x=width-diff
        y=height
        w = 0
        h = diff//2
    
    top_edge = center_y -w -y//2
    left_edge = center_x -h -x//2
    
    bottom_edge = center_y +w +y//2
    right_edge = center_x +h +x//2
    
    crop = img[top_edge:bottom_edge, left_edge:right_edge]

    image_name= folder+'/'+pathlib.Path(image).name.split('.')[0]+'_cropped.'+oxt

    cv.imwrite(image_name, crop)
          
        
def parallel_slicer(files, JOBS, func):
    from joblib import Parallel, delayed
    Parallel (n_jobs=JOBS)(delayed(func)(files[i])
                            for i in range(len(files)))

    

def chunk_creator(item_list, chunksize):
    import itertools
    it = iter(item_list)
    while True:
        chunk = tuple(itertools.islice(it, chunksize))
        if not chunk:
            break
        yield chunk


def main ():
    image_list = get_paths(PATH,ixt)
    from tqdm import tqdm
    import psutil
    JOBS=psutil.cpu_count(logical=True)
    # JOBS = 2
    
    with tqdm(total=len(image_list),
             desc = 'Squaring Images',
             unit='File') as pbar:
        
        filerange = len(image_list)
        chunksize = round(filerange/JOBS)
        if chunksize <1:
            chunksize=1
            JOBS = filerange
        chunks = []
        
        f1 = cropper
        f2 = square_crop
        if res in ['yes', 'y']:
            func = f1
        else:
            func = f2
            
        for c in chunk_creator(image_list, JOBS):
            chunks.append(c)
    
        for i in range(len(chunks)):
            files = chunks[i]
            print('\nRendering: ', files)
            parallel_slicer(files, JOBS, func)
            pbar.update(JOBS)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--PATH', help='Directory with the files to be cropped')
    parser.add_argument('--res', help='Resize all images to 900x900 pixels (Y/y or N/n')
    parser.add_argument('--ixt', help='input file format (tiff,png,jpg')
    parser.add_argument('--oxt', help='output file format (tiff,png,jpg')
    
    args = parser.parse_args()  
    PATH = args.PATH
    res = args.res
    ixt = args.ixt
    oxt = args.oxt
    
    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Please select the folder with the files to be resized")
        print('Working folder:', PATH)
    if res is None:
        res = answer('Resize all images to 900x900? ')  
    
    if ixt is None:
     while ixt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
         print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
         ixt = input('Enter input image format: ')
    
    if oxt is None:
     while oxt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
         print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
         oxt = input('Enter output image format: ')
    
    os.chdir(PATH)

    folder = make_folder('squared')
    
    
    main()