#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: ImgUtils module containing various function for manipulate images
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Mon Oct 12 16:47:44 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
import os
import numpy as np
import cv2 as cv
# from PIL import Image
# Image.MAX_IMAGE_PIXELS = None
import rasterio as rio
from rasterio.plot import reshape_as_raster#, reshape_as_image
from rasterio.windows import Window
from rasterio.enums import Resampling
from utils.TileFuncs import Dim2Tile, TileNumCheck
from rasterio.plot import reshape_as_image#, reshape_as_raster
import gc

def geoslicer(img, dst_width, trs, dst_height, src_crs, max_dim,savename, oxt):
    # from datetime import datetime as dt
    # start = dt.now()
    from rasterio.windows import Window
    import math
   

    
    cnt, height, width = img.shape
    crs = src_crs
    # dtp = src.dtypes[0]
    
          
    vt=Dim2Tile(max_dim, dst_width)
    ht = Dim2Tile(max_dim, dst_height)
    vt, ht = TileNumCheck(vt,ht, dst_width, dst_height, max_dim)
    # if dst_width/vt >1:
    #     vt+=1
    # if dst_height/ht >1:
    #     ht+=1
        
        
    names =[]
    windows =[]
    transforms=[]
     
    
    for ih in range(ht):
        
        for iw in range(vt):
            sname = savename+'_H'+str(ih)+'_V'+str(iw)+'.'+oxt
            names.append(sname)

            x = math.floor(width/vt*iw)
            y = math.floor(height/ht*ih)
            h = math.floor(height/ht)
            w = math.floor(width/vt)

            win = Window(x,y,w,h)
            windows.append(win)
            t= rio.windows.transform(win, trs)
            # t = src.window_transform(win)
            transforms.append(t)
     
    tiles_dict = {'Names':names,
                  'Windows':windows,
                  'Transforms':transforms}
           
    for i in range(len(tiles_dict['Names'])):
            # start=dt.now()
            save_name = tiles_dict['Names'][i]
            win = tiles_dict['Windows'][i]
            tr = tiles_dict['Transforms'][i]
            xx = win.col_off
            yy = win.row_off
            hh = win.height
            ww = win.width
            tile = img[:,yy:yy+hh, xx:xx+ww]
            tile = reshape_as_image(tile)
            tile = cv.normalize(tile, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
            maxval = tile.max()
            if maxval != 0:
                tile = cv.convertScaleAbs(tile, alpha=(255.0/maxval))
            
            with rio.open(save_name,'w',
                     driver='GTiff',
                     width=tile.shape[1],
                     height=tile.shape[0],
                     count=cnt,
                     dtype='uint8',
                     transform=tr,
                     crs=crs) as dst:
               dst.write(tile,indexes = cnt)
            del tile
            gc.collect()
    gc.collect()
    
    

    

# def ImgWriter(save_name, img, img_crs, tile_transform, ext, f1):
#     if ext == 'tiff':
#         drv = 'GTiff'
#     elif ext == 'png':
#         drv='PNG'
#     elif ext == 'jpg':
#         drv='JPEG'
#     if f1 ==1:
#         cnt = img.shape[0]
#         drv='GTiff'
#         sname = save_name+'tiff'
#     else:
#         try:
#             cnt=img.shape[2]
#         except:
#             cnt=1
#         sname = save_name+ext
#     if cnt ==1:
#         h=0
#         w=1
#     else:
#         h=1
#         w=2
#     with rio.open(sname, 'w',
#                               driver = drv,
#                               height= img.shape[h],
#                               width=img.shape[w],
#                               count=cnt,
#                               dtype=img.dtype,
#                               crs=img_crs,
#                               transform=tile_transform) as dst:
#                     if f1==1:
#                         dst.write(img)
#                     else:
#                         dst.write(img,cnt)


         
def InfImgWriter(source, save_path, image):
    from adds.inf2shp import get_world_file, getAffine
    basename = os.path.basename(save_path)
    split = basename.split('.')
    ext = split[len(split)-1]
    src_basename = source + '/'+split[0]
    src_image = src_basename+'.'+ext    
    im = rio.open(src_image)
    img_crs = im.crs
    if img_crs == None:
        crs_file=src_basename+'.wkt'
        with open(crs_file, "r") as f:
            img_crs = f.read()
    trs = im.transform
    if trs == None:
        _,wrf=get_world_file(ext)
        world_file = src_basename+wrf
        trs=getAffine(world_file)
    imm = reshape_as_raster(image)
    savename = save_path.split(ext)[0]
    ImgWriter(savename, imm, img_crs, trs, ext,1)
    

                     
# def Area(chkImage):
#     try:
#         chkImg = Image.fromarray(chkImage)
#     except:
#         chkImg = chkImage
        
#     width, height = chkImg.size
#     area = width*height
#     return(area)

# def ImageBorderErode(image, pixels):
#     Image.MAX_IMAGE_PIXELS = None
#     img = Image.open(image)
#     width, height = img.size
#     left = pixels
#     top = pixels
#     right = width-pixels
#     bot = height-pixels
#     img_precrop= img.crop((left, top, right, bot))
#     im = np.array(img_precrop)
#     return(img_precrop, im)                

def CvContourCrop(processed_image):
    _, threshold = cv.threshold(processed_image, 1, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    x, y, w, h = cv.boundingRect(best_cnt)
    crd = [x,y,w,h]
    img_crop = processed_image[y:y+h, x:x+w,:]
    return(img_crop, crd)

def maxRectContourCrop(processed_image):
    _, bins = cv.threshold(processed_image, 1, 255, cv.THRESH_BINARY)
    #bins = cv.dilate(bins, None)
    #bins = cv.erode(bins, None)
    contours, hierarchy = cv.findContours(bins, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    from maxrect import get_intersection, get_maximal_rectangle
    coords = coordFinder(contours, processed_image)
    _, coordinates = get_intersection([coords])
    coo = list(coordinates)
    ll, ur = get_maximal_rectangle(coo)
    bx = (ll[0],ll[1],ur[0],ur[1])
    bx = [round(num) for num in bx]
    # image = Image.fromarray(processed_image)
    # img_crop = image.crop(bx)  
    return(bx)#img_crop, bx)

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
                # String containing the coordinates. 
                coords.append([int(x),int(y)])
            i = i + 1
    return(coords)
           
def square_crop(image):#, ext, folder):
    src_img = rio.open(image)
    height, width = src_img.shape
    center_x = width/2
    center_y = height/2    
    diff = abs(width-height)
    if width < height:
        # print('a')
        x= width
        y=height-diff
        w = diff//2
        
    elif width > height:
        # print('b')
        x=width-diff
        y=height
        w = 0
    top_edge = center_y - y//2
    left_edge = center_x - x//2
    right_edge = center_x +x//2
    size = right_edge -left_edge
    win = Window(left_edge,top_edge,size,size)
    cnt=src_img.count
    # crs=src_img.crs
    dtp = src_img.dtypes[0]
    t = src_img.window_transform(win)
    # image_name = image.split('.png')[0]
    # savename=folder+'/'+image_name+'_squared.'+ext
    del src_img
    # with rio.open(image) as src:
        # w = src.read(1, window=win)
    return(win, size, cnt, dtp, t)
        # with rio.open(savename,'w',
        #           driver='GTiff',
        #           width=size,
        #           height=size,
        #           count=cnt,
        #           dtype=dtp,
        #           transform=t,
        #           crs=crs) as dst:
        #     dst.write(w,cnt)

def GTiffImageResizer(image, dim):
    with rio.open(image) as src:
        width, height = src.shape
        new_height=dim
        new_width = int(width*new_height/height)
        cnt = src.count
        t = src.transform
        
        img = src.read(
                out_shape=(cnt, new_height, new_width),
                resampling=Resampling.nearest,
            )
        
        transform = t * src.transform.scale(
                new_width,
                new_height)
        src.close()
    return(img, transform, cnt)
    

    
    
def ImgWriter(img, savename, driver, cnt,dtp,transform, crs):
    width, height = img.shape
    with rio.open(savename,'w',
              driver='GTiff',
              width=width,
              height=height,
              count=cnt,
              dtype=dtp,
              transform=transform,
              crs=crs) as dst:
        dst.write(img)
    


def imgNorm(image, image_dir, name):
    import cv2 as cv
    image_norm= cv.normalize(image, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    name_norm=image_dir+name+'_normalized.png'
    cv.imwrite(name_norm,image_norm)
    return(image_norm)

def imgScaler(image, image_dir,name):
    from sklearn import preprocessing 
    min_max_scaler = preprocessing.MinMaxScaler()
    img_norm = (min_max_scaler.fit_transform(image)*255).astype(np.uint8)
    name_scal = image_dir+name+'_scaled.png'
    cv.imwrite(name_scal, img_norm)
    
def imgDen(image, image_dir, name):
    import cv2 as cv
    image_den = cv.fastNlMeansDenoising((image).astype(np.uint8), None, 10,7,21)
    name_den=name+'_denoised.png'
    cv.imwrite(name_den, image_den)

def imgEnh(image, name):
    if isinstance(image, list):
        img_norm = []
        for im in image:
            img_norm.append(cv.normalize(im, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX))
        img_merge=(img_norm[0]+img_norm[1])*2
        cv.imwrite('Merged2.png',img_merge)
