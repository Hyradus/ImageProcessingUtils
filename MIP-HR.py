#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Multi Image Parallel Resizer
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de

Script to resize given images to user height

Created on Tue Aug 11 18:46:42 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""


import os 
from datetime import datetime
import shutil
from PIL import Image
import pathlib
from tkinter import Tk,filedialog
from argparse import ArgumentParser

global PATH
global folder
global nh
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

def get_paths(PATH, ixt):
    import glob
    os.chdir(PATH)
    filename = [i for i in glob.glob('**/*.'+ixt,recursive=True)]
    return(filename)




def resizer(image):
    
    from PIL import ImageOps
    Image.MAX_IMAGE_PIXELS = None

    img = Image.open(image)

    width= img.size[0]
    height=img.size[1]
    nw=int(width*nh/height)
    size = (nw,nh)
    img = ImageOps.fit(img, size, Image.ANTIALIAS)
    image_name= folder+'/'+pathlib.Path(image).name.split('.')[0]+'_resized.'+oxt
    img.save(image_name)
    
              
def parallel_resizer(files, JOBS):
    from joblib import Parallel, delayed
    Parallel (n_jobs=JOBS)(delayed(resizer)(files[i])
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
    image_list = get_paths(PATH, ixt)
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
        
                    
        for c in chunk_creator(image_list, JOBS):
            chunks.append(c)
    
        for i in range(len(chunks)):
            files = chunks[i]
            print('\nResizing: ', files)
            parallel_resizer(files, JOBS)
            pbar.update(JOBS)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--PATH', help='Directory with the files to be cropped')
    parser.add_argument('--nh', help='New height in pixels')
    parser.add_argument('--ixt', help='input file format (tiff,png,jpg')
    parser.add_argument('--oxt', help='output file format (tiff,png,jpg')
    
    args = parser.parse_args()  
    PATH = args.PATH
    nh = args.nh
    ixt = args.ixt
    oxt = args.oxt
    
    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Please select the folder with the files to be resized")
        print('Working folder:', PATH)
    if nh is None:
        nh=int(input('Please insert new height in pixels: '))
    
    if ixt is None:
     while ixt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
         print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
         ixt = input('Enter input image format: ')
    
    if oxt is None:
     while oxt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
         print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
         oxt = input('Enter output image format: ')
    
    
    os.chdir(PATH)

    folder = make_folder('resized')
    
    
    main()