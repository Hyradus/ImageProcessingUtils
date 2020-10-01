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

import cv2 as cv
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from datetime import datetime
import shutil
import pathlib
import os
from argparse import ArgumentParser
from tkinter import Tk,filedialog

from utils import question, make_folder, get_paths, Area, ImageBorderErode, chunk_creator
from ContoursCropper import CvContourCrop, maxRectContourCrop

global contour_folder
global crop_folder
global biggest_contour
global img
global img_precrop
global im
global ixt
global oxt

# def answer(question):
#     answ = None
#     while answ not in ['yes','y','no','n']:
#         print("Please enter yes/y or no/n.")
#         answ = input(question+': ')
#     return(answ)

# def make_folder(name):
#     os.getcwd()
#     folder = name
#     if os.path.exists(folder):
#            qst = name + ' Folder exist, remove it? '
#            answ = answer(qst)
#            if answ in ['yes', 'y']:
#                shutil.rmtree(folder)
#                os.mkdir(folder)
#                print(name, 'Folder created')
#            else:
#                now = datetime.now()
#                folder = name +'_' + now.strftime("%d-%m-%Y_%H-%M-%S")
#                print(folder, ' Folder not exist, creating.')
#                os.mkdir(folder)
#                print('Created new ', name,' Folder')
#     else:
#         print(name, ' Folder not exist, creating.')
#         os.mkdir(folder)
#         print('Created new ', name,' Folder')
#     return(folder)

# def get_paths(PATH, ixt):
#     import glob
#     os.chdir(PATH)
#     filename = [i for i in glob.glob('**/*.'+ixt,recursive=True)]
#     return(filename)

def preprocess(image):
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(image)
    
    width, height = img.size
    
    left = 200
    top = 200
    right = width-200
    bot = height-200
    img_precrop= img.crop((left, top, right, bot))
    im = np.array(img_precrop)
    return(img_precrop, im)
    
    
def coordFinder(contours, gray):
    for cnt in contours : 
  
        approx = cv.approxPolyDP(cnt, 0.009 * cv.arcLength(cnt, True), True) 
      
        n = approx.ravel()  
        i = 0
        coords =[]
        for j in n : 
            if(i % 2 == 0): 
                x = n[i] 
                y = n[i + 1] 
      
                # String containing the co-ordinates. 
                coords.append([int(x),int(y)])
            i = i + 1
    return(coords)

def chkSize(chkImage):
    try:
        chkImg = Image.fromarray(chkImage)
    except:
        chkImg = chkImage
        
    width, height = chkImg.size
    area = width*height
    
    return(area)
def CCROP(img_precrop, image_name):
    imm = np.array(img_precrop)
    _, threshold = cv.threshold(imm, 1, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # find the contour with the highest area, that will be
    # a slightly too big crop of what we need
    max_area = 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
            
    # crop it like this so we can perform additional operations
    # to further narrow down the crop
    x, y, w, h = cv.boundingRect(best_cnt)
    gray_crop = imm[y:y+h, x:x+w]
    _, bins = cv.threshold(gray_crop, 1, 255, cv.THRESH_BINARY)
    bins = cv.dilate(bins, None)  # fill some holes

    bins = cv.erode(bins, None)   # dilate made our shape larger, revert that
    contours, hierarchy = cv.findContours(bins, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    from maxrect import get_intersection, get_maximal_rectangle
  
    coords = coordFinder(contours, gray_crop)
    _, coordinates = get_intersection([coords])
    coo = list(coordinates)

    ll, ur = get_maximal_rectangle(coo)
    bx = (ll[0],ll[1],ur[0],ur[1])
    image = Image.fromarray(gray_crop)
    im_crop = image.crop(bx)  
    area = chkSize(im_crop)
    if area <= 1048576:
        print("\nImage smaller than 1024*1024, skipping...")
    else:
        
        savename=crop_folder+'/'+image_name+'_crop.png'
        im_crop.save(savename)
    
def chksize(chkImage):
    try:
        chkImg = Image.fromarray(chkImage)
    except:
        chkImg = chkImage
        
    width, height = chkImg.shape
    area = width*height
    
    return(area)
    
  

def contour_crop(image):
    image_name= pathlib.Path(image).name.split('.')[0]
    img_precrop, im= preprocess(image)
    # img_precrop, im= ImageBorderErode(image, 100)
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
   
# def chunk_creator(item_list, chunksize):
#     import itertools
#     it = iter(item_list)
#     while True:
#         chunk = tuple(itertools.islice(it, chunksize))
#         if not chunk:
#             break
#         yield chunk

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
    
    # contour_folder = make_folder('contours')
    crop_folder = make_folder(PATH,'cropped')
    
    
    main()