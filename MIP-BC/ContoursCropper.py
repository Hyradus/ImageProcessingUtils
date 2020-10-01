#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Mon Sep 28 21:10:00 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
import cv2 as cv
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

def CvContourCrop(processed_image):
    _, threshold = cv.threshold(processed_image, 1, 255, cv.THRESH_BINARY)
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
    img_crop = processed_image[y:y+h, x:x+w]
    return(img_crop)

def maxRectContourCrop(processed_image):
    _, bins = cv.threshold(processed_image, 1, 255, cv.THRESH_BINARY)
    bins = cv.dilate(bins, None)  # fill some holes

    bins = cv.erode(bins, None)   # dilate made our shape larger, revert that
    contours, hierarchy = cv.findContours(bins, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    from maxrect import get_intersection, get_maximal_rectangle
  
    coords = coordFinder(contours, processed_image)
    _, coordinates = get_intersection([coords])
    coo = list(coordinates)

    ll, ur = get_maximal_rectangle(coo)
    bx = (ll[0],ll[1],ur[0],ur[1])
    image = Image.fromarray(processed_image)
    img_crop = image.crop(bx)  
    return(img_crop)


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
