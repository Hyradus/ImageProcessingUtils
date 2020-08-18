#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Multi image resizer 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Tue Aug 11 18:46:42 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""


import os 
from datetime import datetime
import shutil
# from PIL import Image
import cv2 as cv

global folder
import pathlib
global max_height

PATH = '/media/gnodj/W-DATS/DeepLearning/Tensorflow/HiRiSE_Dataset/HIRISE_JP2/PNGs'
# max_width = 640
max_height = 3600

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


image_list = get_paths(PATH, 'png') #edit image file extension

os.chdir(PATH)
folder = make_folder('Resized')

def resizer(image):
    print('\nResizing: ', image)
    img = cv.imread(image)
    
    width = img.shape[1]
    height = img.shape[0]
    
    new_width = int(width*max_height/height)   
    dim = (new_width, max_height)
    # new_height = int(max_width*height/width)
    # dim = (max_width, new_height)
    img_res = cv.resize(img, dim, interpolation = cv.INTER_NEAREST)
    image_name= 'Resized/'+pathlib.Path(image).name.split('.')[0]+'_resized.png'
    # shutil.move(image, folder)
    cv.imwrite(image_name, img_res)
        
        
def parallel_slicer(files, JOBS):
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
        parallel_slicer(files, JOBS)
        pbar.update(JOBS)
