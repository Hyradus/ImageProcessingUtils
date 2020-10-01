#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Mon Sep 28 18:45:02 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
import os
import shutil
from datetime import datetime
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import numpy as np


def question(question, answers):
    answ = None
    while answ not in answers:
        print('Please enter only: ')
        print(*answers, sep=', ')
        
        answ = input(question+'Answer: ')
    return(answ)

def make_folder(path, name):
    #os.getcwd()
    folder = path+'/'+name
    if os.path.exists(folder):
           qst = name + ' Folder exist, remove it? '
           answ = question(qst,['yes','y','no','n'])
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


def intInput(w):
    while True:
        try:
            ask='Insert '+w+': '
            intInpt = int(input(ask))
        except:
            print('Please insert only one integer')
            # continue
        if isinstance(intInpt, int):
                    break
    return(intInpt)

def Area(chkImage):
    try:
        chkImg = Image.fromarray(chkImage)
    except:
        chkImg = chkImage
        
    width, height = chkImg.size
    area = width*height
    
    return(area)

def ImageBorderErode(image, pixels):
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(image)
    
    width, height = img.size
    
    left = pixels
    top = pixels
    right = width-pixels
    bot = height-pixels
    img_precrop= img.crop((left, top, right, bot))
    im = np.array(img_precrop)
    return(img_precrop, im)

def chunk_creator(item_list, chunksize):
    import itertools
    it = iter(item_list)
    while True:
        chunk = tuple(itertools.islice(it, chunksize))
        if not chunk:
            break
        yield chunk
