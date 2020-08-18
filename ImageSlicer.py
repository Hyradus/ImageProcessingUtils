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

Image.MAX_IMAGE_PIXELS = None
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
               new_name = name +'_' + now.strftime("%d-%m-%Y_%H-%M-%S")
               print(new_name, ' Folder not exist, creating.')
               os.mkdir(new_name)
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


image_list = get_paths(PATH, 'png') # edit image extension

os.chdir(PATH)
folder = make_folder('Processed')
tiles = 10
for image in image_list:
    print('\nSlicing: ', image, ' in ', tiles, ' tiles.')
    ims.slice(image, tiles)
    shutil.move(image, folder)
