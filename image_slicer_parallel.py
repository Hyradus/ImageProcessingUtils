#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Multi image slicer
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Tue Aug 11 18:46:42 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""

import image_slicer as ims
import os 
from datetime import datetime
import shutil
from PIL import Image


PATH = #INSERT PATH TO FILE DIRECTORY

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
global folder
global tiles

os.chdir(PATH)
folder = make_folder('Processed')
tiles = 10

def slicer(image):
    print('\nSlicing: ', image, ' in ', tiles, ' tiles.')
    Image.MAX_IMAGE_PIXELS = None
    ims.slice(image, tiles)
    shutil.move(image, folder)

def parallel_slicer(files, JOBS):
    from joblib import Parallel, delayed
    Parallel (n_jobs=JOBS)(delayed(slicer)(files[i])
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
