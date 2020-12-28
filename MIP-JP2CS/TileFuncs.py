#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Mon Sep 28 11:58:29 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
from ImgUtils import Area

def Dim2Tile(min_val, dimension):
    tile = int(round(dimension/min_val,0))   
    return(tile)


from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import numpy as np 
    
import cv2 as cv


def TileCheckSave(img, save_name, vt, ht, iw, ih):
    width, height = img.size
    x = int(width/vt*iw)
    y = int(height/ht*ih)
    h = int((height/ht))
    w = int((width/vt))

    im = np.array(img)
    tile = im[y:y+h, x:x+w]
    area = Area(tile)
    if area <8192:
        print("\nImage too small, skipping...", area,' pixels')
    else:
        cv.imwrite(save_name,tile)


def TileNumCheck(tilenum, dimension, size):
    if dimension/tilenum < size:
        tilenum = tilenum -1
    return(tilenum)
