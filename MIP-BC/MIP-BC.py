#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Multi Image Parallel Borders/BackGround Cropper
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de

This script try to crop images that have black background borders into rectangular
images with no borders. (TO BE improoved)



Created on Sat Aug 22 17:39:27 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""

import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

import pathlib
import os
from argparse import ArgumentParser
from tkinter import Tk,filedialog


from utils import make_folder, get_paths, Area, chunk_creator, ImageBorderErode
from ContoursCropper import CvContourCrop, maxRectContourCrop, coordFinder

global contour_folder
global crop_folder
global biggest_contour
global img
global img_precrop
global im
global ixt
global oxt
   



def CCROP(img_precrop, image_name):
    image = np.array(img_precrop)
    cv_crop=CvContourCrop(image)
    maxRectCrop = maxRectContourCrop(cv_crop)
    
    area = Area(maxRectCrop)
    if area <= 1048576:
        print("\nImage smaller than 1024*1024, skipping...")
    else:
        
        savename=crop_folder+'/'+image_name+'_crop.png'
        maxRectCrop.save(savename)


def contour_crop(image):
    image_name= pathlib.Path(image).name.split('.')[0]
    img_precrop, im= ImageBorderErode(image, 100)
  
    try:
        CCROP(img_precrop,image_name)
    except:
        print('error')
        savename = crop_folder+'/'+image_name+'.png'
        img_precrop.save(savename)        
        print('\n Skipped: ', image_name)


def parallel_contour(files, JOBS):
    from joblib import Parallel, delayed
    Parallel (n_jobs=JOBS)(delayed(contour_crop)(files[i])
                            for i in range(len(files)))

def main():
        
    image_list = get_paths(PATH, ixt) #edit image file extension
    
    from tqdm import tqdm
    import psutil
    JOBS=psutil.cpu_count(logical=True)
    # JOBS = 2
    
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
            print('\nRendering: ', files)
            
            parallel_contour(files, JOBS)
            pbar.update(JOBS)
            

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--PATH', help='Directory with the files to be cropped as square')
    parser.add_argument('--ixt', help='output file format (tiff,png,jpg')
    parser.add_argument('--oxt', help='output file format (tiff,png,jpg')
    args = parser.parse_args()  
    PATH = args.PATH
    ixt = args.ixt
    oxt = args.oxt
    
    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Please select the folder with the files to be cropped as square")
        print('Working folder:', PATH)
    if ixt is None:
        while ixt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
         print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
         ixt = input('Enter input image format: ')
         
    if oxt is None:
        while oxt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
            print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
            oxt = input('Enter output image format: ')
    # os.chdir(PATH)
    
    crop_folder = make_folder(PATH, 'cropped')
    
    
    main()