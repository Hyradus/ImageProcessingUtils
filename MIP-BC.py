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


global contour_folder
global crop_folder
global biggest_contour
global img
global img_precrop
global im
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

def preprocess(image):
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(image)
    
    width, height = img.size
    
    left = 0
    top = 50
    right = width
    bot = height-50
    img_precrop= img.crop((left, top, right, bot))
    im = np.array(img_precrop)
    return(img_precrop, im)
    
    
def contour(img_precrop, im, image_name):

    imm = np.array(img_precrop)
    try:
        gray = cv.cvtColor(imm, cv.COLOR_BGR2GRAY)
    except:
        gray=imm
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    # _, bins = cv.threshold(gray,0,1,0) # inverted threshold (light obj on dark bg)
    _, bins = cv.threshold(gray, 0, 1, cv.THRESH_BINARY)
    bins = cv.dilate(bins, None)  # fill some holes
    bins = cv.dilate(bins, None)
    bins = cv.dilate(bins, None)
    bins = cv.dilate(bins, None)
    bins = cv.erode(bins, None)   # dilate made our shape larger, revert that
    bins = cv.erode(bins, None)
    contours, hierarchy = cv.findContours(bins, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contour_sizes = [(cv.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    
    cv.drawContours(imm, biggest_contour, -1, (0,255,0), 25)
    savename=contour_folder+'/'+image_name+'_contours.'+oxt
    cv.imwrite(savename, imm)
    return(biggest_contour)

def extPT(biggest_contour):
    bc = biggest_contour
    extLeft = tuple(bc[bc[:, :, 0].argmin()][0])
    extRight = tuple(bc[bc[:, :, 0].argmax()][0])
    extTop = tuple(bc[bc[:, :, 1].argmin()][0])
    extBot = tuple(bc[bc[:, :, 1].argmax()][0])
    rect = cv.minAreaRect(biggest_contour)
    box = cv.boxPoints(rect)
    box = np.int0(box)
    return(extLeft, extRight, extTop, extBot, box)

def crop(biggest_contour, img_precrop, image_name):
    extLeft, extRight, extTop, extBot, box = extPT(biggest_contour)
        
    
    savename=crop_folder+'/'+image_name+'_crop.png'
    
    bx1 = (box[0][0], box[1][1], box[2][0], box[3][1])
    im_crop = img_precrop.crop(bx1)
    width = im_crop.size[0]
    height = im_crop.size[1]
    
    
    if width ==0 or height==0:    
        bx2 =(extBot[0], extLeft[1], extTop[0], extRight[1])
        # bx2 =(extLeft[0], extLeft[1], extRight[0], extRight[1])
        im_crop = img_precrop.crop(bx2)
        width = im_crop.size[0]
        height = im_crop.size[1]
        # print('1')
        
    if width ==0 or height==0:
        # bx3 =(extBot[0], extLeft[1], extRight[0], extBot[1])
        bx3 =(extBot[0], extLeft[1], extRight[0], extRight[1])
        im_crop = img_precrop.crop(bx3)
        # im_crop = img_precrop.crop((extBot[0], extLeft[1], extTop[0], extRight[1]))
        width = im_crop.size[0]
        height = im_crop.size[1]
        # print('2')
        
    if width ==0 or height==0:
        print('\nNothing to crop')
        src=image_name+'.'+oxt
        dest=crop_folder+'/'+src
        shutil.copyfile(src, dest)
    else:
        im_crop.save(savename)
    
                
    # try:
    #     bx =  (box[0][0], box[1][1], box[2][0], box[3][1])
    #     im_crop = img_precrop.crop(bx)
    #     # if im_crop.size[0]==0 or im_crop.size[1]==0:
        
    # except:
    #     # im_crop = img_precrop.crop((extBot[0], extLeft[1], extTop[0], extRight[1]))
    #     bx =(extBot[0], extLeft[1], extTop[0], extRight[1])
    #     im_crop = img_precrop.crop(bx)
        
    #     bx =(extBot[0], extLeft[1], extRight[0], extBot[1])
  
   

def contour_crop(image):
    image_name= pathlib.Path(image).name.split('.')[0]
    img_precrop, im = preprocess(image)
    biggest_contour=contour(img_precrop, im, image_name)
    crop(biggest_contour, img_precrop, image_name)
        
def parallel_contour(files, JOBS):
    from joblib import Parallel, delayed
    Parallel (n_jobs=JOBS)(delayed(contour_crop)(files[i])
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
    os.chdir(PATH)
    
    contour_folder = make_folder('contours')
    crop_folder = make_folder('cropped')
    
    
    main()