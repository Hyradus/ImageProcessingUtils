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
import os
from argparse import ArgumentParser
from copy import copy
from tkinter import Tk,filedialog
from utils.GenUtils import get_paths, chunk_creator, folder_file_size, question
from utils.ImgUtils import square_crop, geoslicer, borderCropper, CellSizeScale
import rasterio as rio
from rasterio.enums import Resampling
from rasterio.windows import Window
import cv2 as cv
global dst_folder
global ixt
global oxt
# global cell
# global res_size
# global crp
# global bc
# global lim
# global limit_size
global dst_folder
import pandas as pd
global proc_df
#import numpy as np

def cropper(image, bc, sqcrp, res, cell_size, lim, limit_size):
    image_name = os.path.basename(image).split('.')[0]#+ixt
    savename=dst_folder+'/'+image_name
    data_dict = {'Name': image_name} 
    tmp_df = pd.DataFrame.from_dict([data_dict])
    try:
        with rio.open(image) as src:
          
            src_height, src_width = src.shape
            crs = src.crs
            cnt = src.count
            src_trs = src.transform
            dst_trs = copy(src_trs)
            xoff = 0
            yoff = 0
            src_win = Window(xoff,yoff,src.width,src_height)
            # dst_win = copy(src_win)
            if cell_size == None:
               cell_size = src.transform[0]
            
            if lim in ['Y','y']:
                if src_width > int(limit_size) or src_height >int(limit_size):
                    # src_crs = src.crs
                    max_dim = int(limit_size)
                    geoslicer(image, max_dim, savename, bc, sqcrp, res, cell_size, oxt)

            else:
                
                if bc in ['y','y']:
                    try:
                        src_width, src_height, src_win, dst_trs, savename =  borderCropper(src, src_win, savename)
                    except Exception as e:
                        print(e)
                        pass
                    
                if sqcrp in ['Y','y']:

                    try:
                       src_width, src_height, src_win, dst_trs, savename = square_crop(src,
                                                                              src_width,
                                                                              src_height,
                                                                              src_win,
                                                                              # xoff,
                                                                              # yoff,
                                                                              savename)
                    except Exception as e:
                        print(e)
                        pass
                    
                    
                    
               
                if res in ['Y', 'y']:
                    try:
                        src_height, src_width, dst_trs, savename = CellSizeScale(src,
                                                                                 src_height,
                                                                                 src_width,
                                                                                 float(cell_size),
                                                                                 dst_trs,
                                                                                 savename)
                    except Exception as e:
                        print(e)
                        pass
    
                try:
                    img = src.read(window=src_win,
                                   out_shape=(cnt, src_height, src_width),
                                   resampling=Resampling.cubic)
                    img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
                    maxval = img.max()
                    
                    if maxval != 0:
                        alpha = alpha=(255.0/maxval)
                        img = cv.convertScaleAbs(img, alpha=alpha) 
                        savename = savename+'.'+oxt
                        # print(savename)
                        with rio.open(savename,'w',
                                  driver='GTiff',
                                  window=src_win,
                                  width=src_width,
                                  height=src_height,
                                  count=cnt,
                                  dtype=img.dtype,
                                  transform=dst_trs,
                                  crs=crs) as dst:
                            dst.write(img)
                except Exception as e:
                    print(e)
                
                tmp_df = pd.DataFrame.from_dict([data_dict])                    
                return tmp_df
    except Exception as e:
        print(e)
        pass



def parallel_crops(files, JOBS, bc, sqcrp, res, cell_size, lim, limit_size):
    from joblib import Parallel, delayed
    tmp_df = Parallel (n_jobs=JOBS)(delayed(cropper)(files[i],
                                                     bc, sqcrp,
                                                     res, cell_size,
                                                     lim, limit_size)
                            for i in range(len(files)))
    return tmp_df

def main():
        
    image_list = get_paths(PATH, ixt) 
    total_size, max_size, av_fsize = folder_file_size(PATH,image_list)

    from tqdm import tqdm
    import psutil
    
    avram=psutil.virtual_memory().total >> 30
    avcores=psutil.cpu_count(logical=False)
    avthreads=psutil.cpu_count(logical=True)
    ram_thread = avram/avthreads
    req_mem = avthreads*max_size
    if req_mem > avcores and req_mem > avram:
        JOBS = avcores
    else:
        JOBS = avcores
    
        
    if ram_thread > 2:
        JOBS=avcores
    
    # cols = ['Name','Processed']
    proc_csv = dst_folder+'/Processed.csv'
    try:
        proc_df = pd.read_csv(proc_csv)
    except Exception as e:
        print(e)
        proc_df = pd.DataFrame(columns=['Name'])
    pass
    
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
            lambda_f = lambda element:(os.path.basename(element).split('.')[0]) not in proc_df['Name'].to_list()
            # filtered = [path for path in files if os.path.basename(path).split(ixt)[0] not in proc_df['Name'].to_list()]
            filtered = filter(lambda_f, files)
            #for proc in proc_df['Name'].tolist():
                #chunk_filter = lambda element: element != proc
                #filtered = filter(chunk_filter, proc)
            chunk = list(filtered)
            if len(chunk)>0:
               tmp_df = parallel_crops(files, JOBS, bc, sqcrp, res, cell_size, lim, limit_size)
               for df in tmp_df:
                   proc_df = proc_df.append(df,ignore_index=True)
               #proc_df = proc_df.append(tmp_df,ignore_index=True)
               proc_df.to_csv(proc_csv, index=False)
               pbar.update(JOBS)
            else:
                pbar.update(len(files))
                continue
            

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--PATH', help='Directory with the files to be cropped as square')
    parser.add_argument('--dst', help='Destination folder, if empty PATH is used')
    parser.add_argument('--ixt', help='output file format (tiff,png,jpg')
    parser.add_argument('--oxt', help='output file format (tiff,png,jpg')
    parser.add_argument('--bc', help='Remove black borders? Y/y or N/n')
    parser.add_argument('--res', help='resize images? Y/y or N/n')
    parser.add_argument('--cs', help='cell size in m')
    parser.add_argument('--sqcrop', help='Center crop images? Y/y or N/n')
    parser.add_argument('--lim', help='Specify limit size for images? Y/y or N/n')
    parser.add_argument('--px', help='Limit size in pixel')
    args = parser.parse_args()  
    PATH = args.PATH
    dst_folder = args.dst
    ixt = args.ixt
    oxt = args.oxt
    res = args.res
    cell_size = args.cs
    sqcrp = args.sqcrop
    bc = args.bc
    lim = args.lim
    limit_size = args.px
    # fold_name = 'Processed'
    
    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Please select the folder with the files to be cropped as square")
        print('Working folder:', PATH)
        
    if dst_folder is None:
        root = Tk()
        root.withdraw()
        dst_folder = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Select output folder")
        print('Output folder:', dst_folder)
        
    if ixt is None:
        while ixt not in ['TIFF','tiff','PNG','png','JPG','jpg','JP2','jp2']:
         print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
         ixt = input('Enter input image format: ')
         
    if oxt is None:
        while oxt not in ['TIFF','tiff','PNG','png','JPG','jpg']:
            print('Please enter TIFF or tiff, PNG or png or JPG or jpg')    
            oxt = input('Enter output image format: ')
            
    if bc is None:
          q = question('Crop black borders?',['Y','y','N','n'])
          if q in ['Y','y']:
             bc = q
             # fold_name = fold_name+'_bc'
    
         
    if sqcrp is None:
        q = question('Center crop images?',['Y','y','N','n'])
        if q in ['Y','y']:
            sqcrp = q
            # fold_name = fold_name+'_scrp'
    else:
         ccrp = None   
            
    if res is None:
        res = question('Resize images?',['Y','y','N','n'])
    if res in ['Y','y'] and cell_size is None:
        while True:
            cell_size = input('Insert desired cell size in meters to resize images ' )
            try:    
                cell_size=float(cell_size)
                break
            except:
                try:
                    cell_size=int(float(cell_size))
                    break
                except:
                    print('Please enter a valid number')
        # fold_name = fold_name+'_cellsize_'+str(cell_size)+'m'
    # else:
    #     # cell_size = None
    #     # cell_size = 'original'

    if lim is None:
        lim = question('Resize images below a limit?',['Y','y','N','n'])
        
    if lim in ['Y','y'] and limit_size is None:
        while True:
            
            limit_size = input('Insert desired size limit images ' )
            try:    
                limit_size=int(limit_size)
                break
            except:
                try:
                    limit_size=int(float(limit_size))
                    break
                except:
                    print('Please enter a valid number')
        # fold_name = fold_name+'_res_'+str(limit_size)+'px'
    

    
    


    if bc == None and sqcrp == None and cell_size == None and lim == None and res == None:
        print('Please select at least one task')
    else:
        fold_name = 'BC_'+str(bc)+'_SQCRP_'+str(sqcrp)+'_'+'CellSize_'+str(cell_size).replace('.','-')+'_m_'+'_LIM_'+str(lim)+'_'+str(limit_size)+'_px'
        
        if dst_folder == None:
            dst_folder = PATH+'/'+fold_name
        else:
            dst_folder = dst_folder+'/'+fold_name
        os.makedirs(dst_folder, exist_ok=True)
        print(bc)
        # limit_size = int(limit_size)
        # try:
        #     int(cell_size)
        # except:
        #     pass
        # try:
        #     int(limit_size)
        # except:
        #     pass
        
main()
