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
from tkinter import Tk,filedialog
from utils.GenUtils import make_folder, get_paths, chunk_creator, folder_file_size, question
from utils.ImgUtils import square_crop, CvContourCrop, maxRectContourCrop, geoslicer, borderCropper#, ImageResizer, ImgWriter
import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
from rasterio.windows import Window
#from utils.GenUtils import make_folder, get_paths, chunk_creator, folder_file_size
# from utils.ImgUtils import CvContourCrop, maxRectContourCrop, geoslicer
from rasterio.plot import reshape_as_image
import cv2 as cv
global contour_folder
global dst_folder
global biggest_contour
global img
global img_precrop
global im
global ixt
global oxt
global cell_size
global crp
global bc
global lim
global lim_size
import pandas as pd
global proc_df
#import numpy as np

def cropper(image):
    image_name = os.path.basename(image).split('.')[0]#+ixt
    savename=dst_folder+'/'+image_name.split(ixt)[0]
    data_dict = {'Name': image_name} 
    tmp_df = pd.DataFrame.from_dict([data_dict])
        
    
    with rio.open(image) as src:
          
        src_height, src_width = src.shape
        crs = src.crs
        cnt = src.count
        trs = src.transform
        xoff = 0
        yoff = 0
        win = Window(xoff,yoff,src.width,src_height)
       
        if res in ['Y', 'y']:
            # print('res')
            cell_sizeX = abs(src.transform[0])
            cell_sizeY = abs(src.transform[4])
            dst_cell_sizeX = cell_size
            dst_cell_sizeY = cell_size
            scaleX = cell_sizeX/dst_cell_sizeX
            scaleY = cell_sizeY/dst_cell_sizeY
            dst_height=int(src_height*scaleY)
            dst_width=int(src_width*scaleX)
            
            
            trs = trs * src.transform.scale(
                    (src_width/dst_width),
                    (src_height/dst_height)
                )
            # win = Window(xoff, yoff, dst_width, dst_height)
            savename = savename+'_res_'+str(cell_size)+'m'
            
                # img = src.read(window=win,
                #             out_shape=(cnt, dst_height, dst_width),
                #             resampling=Resampling.cubic,
                #         )
                # img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
                # maxval=img.max()
                # if maxval != 0:
                #     img = cv.convertScaleAbs(img, alpha=(255.0/maxval))   
        else:
            dst_width = src_width
            dst_height = src_height
            
        # if lim in ['Y','y']:
        #     # print('lim')
        #     # img = src.read(window=win,
        #     #                    out_shape=(cnt, dst_height, dst_width),
        #     #                    resampling=Resampling.cubic,
        #     #                )
        #     # img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
        #     # maxval=src.read().max()

        #     # if maxval != 0:
        #     #     img = cv.convertScaleAbs(img, alpha=(255.0/maxval))
        #     if dst_width > limit_size or dst_height >limit_size:

        #         # src_crs = src.crs
        #         max_dim = limit_size
        #         # geoslicer(src, dst_width, trs, dst_height, src_crs, max_dim,savename, oxt, bc)
        #         geoslicer(image, dst_width, dst_height, trs,win, max_dim, savename, oxt, bc)
        #     else:
        #              #savename = savename.split(ixt)[0]+'.'+oxt
        #         # savename = savename.split(ixt)[0]+str(maxval)+'px_'
        #         savename = savename+'_'+str(limit_size)+'px'
        #     #         with rio.open(savename,'w',
        #     #                   driver='GTiff',
        #     #                   window=win,
        #     #                   width=dst_width,
        #     #                   height=dst_height,
        #     #                   count=cnt,
        #     #                   dtype='uint8',
        #     #                   transform=trs,
        #     #                   crs=crs) as dst:
        #     #             dst.write(img)
       
                
        # if bc in ['y','y']:
        #     # print('bc')
        #     try:
        #          processed_image = reshape_as_image(src.read(window=win,
        #                                    out_shape=(cnt, dst_height, dst_width),
        #                                    resampling=Resampling.cubic))
        #          dst_height, dst_width, win, savename = borderCropper(processed_image, savename)
        #          trs = rio.windows.transform(win, trs)
        #         # pre_crop, crd = CvContourCrop(np.array(reshape_as_image(src.read()).astype(np.uint8)))
        #         # crop, crd2 = CvContourCrop(pre_crop)
        #         # bx =  maxRectContourCrop(pre_crop)
        #         # del pre_crop
        #         # cnt = src.count
        #         # crs = src.crs
        #         # ysize = bx[3]-bx[1]
        #         # xsize = bx[2]-bx[0]
        #         # xoff = crd[0]+bx[0]
        #         # yoff = crd[1]+bx[1]
        #         # win = Window(xoff, yoff, xsize, ysize)
        #         # trs = src.window_transform(win)
        #         # src_height=ysize
        #         # src_width=xsize
        #         # dst_height=ysize
        #         # dst_width=xsize
        #         # savename = savename+'_cropped'
        #     except Exception as e:
        #         print(e)
        #         pass
            
        # if ccrp in ['Y','y']:
        #     # print('crp')
        #     try:
        #         center_x = dst_width//2
        #         center_y = dst_height//2    
        #         diff = abs(dst_width-dst_height)
        #         if dst_width <= dst_height:
        #             x = dst_width
        #             y = dst_height-diff
                    
        #         elif dst_width > dst_height:
        #             x = dst_width-diff
        #             y = dst_height
                    
        #         top_edge = center_y - y//2+ yoff
        #         left_edge = center_x - x//2 + xoff
        #         right_edge = center_x +x//2 +xoff
        #         size = right_edge -left_edge
        #         size = int(size)
        #         win = Window(left_edge,top_edge,size,size)
        #         trs = src.window_transform(win)
        #         savename = savename+'_centered'
        #     except Exception as e:
        #         print(e)
        #         pass
                
                                        
        print('ciaociao')
        try:
            img = src.read(window=win,
                           out_shape=(cnt, dst_height, dst_width),
                           resampling=Resampling.cubic,
                       )
            img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
            maxval=img.max()
            if maxval != 0:
                img = cv.convertScaleAbs(img, alpha=(255.0/maxval))
            if bc in ['y','y']:
            # print('bc')
             
                dst_height, dst_width, win, savename = borderCropper(reshape_as_image(img), savename)
                trs = rio.windows.transform(win, trs)
            # img = reshape_as_image(img)
            # if lim in ['Y','y']:
            #     if dst_width > limit_size or dst_height >limit_size:

            #         src_crs = src.crs
            #         max_dim = limit_size
            #         geoslicer(img, dst_width, trs, dst_height, src_crs, max_dim,savename, oxt)
            #     else:
            #         savename = savename.split(ixt)[0]+'.'+oxt
            #         with rio.open(savename,'w',
            #                   driver='GTiff',
            #                   window=win,
            #                   width=dst_width,
            #                   height=dst_height,
            #                   count=cnt,
            #                   dtype='uint8',
            #                   transform=trs,
            #                   crs=crs) as dst:
            #             dst.write(img)
            # else:
           
            savename = savename.split(ixt)[0]+str(maxval)+'px_'+'.'+oxt
            print(savename)
            with rio.open(savename,'w',
                      driver='GTiff',
                      window=win,
                      width=dst_width,
                      height=dst_height,
                      count=cnt,
                      dtype='uint8',
                      transform=trs,
                      crs=crs) as dst:
                dst.write(img)
        except Exception as e:
            print(e)
        
        tmp_df = pd.DataFrame.from_dict([data_dict])                    
        return tmp_df


def parallel_crops(files, JOBS):
    from joblib import Parallel, delayed
    tmp_df = Parallel (n_jobs=JOBS)(delayed(cropper)(files[i])
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
               tmp_df = parallel_crops(files, JOBS)
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
    parser.add_argument('--ixt', help='output file format (tiff,png,jpg')
    parser.add_argument('--oxt', help='output file format (tiff,png,jpg')
    parser.add_argument('--bc', help='Remove black borders? Y/y or N/n')
    parser.add_argument('--res', help='resize images? Y/y or N/n')
    parser.add_argument('--ccrop', help='Center crop images? Y/y or N/n')
    parser.add_argument('--lim', help='Specify limit size for images? Y/y or N/n')
    args = parser.parse_args()  
    PATH = args.PATH
    ixt = args.ixt
    oxt = args.oxt
    res = args.res
    ccrp = args.ccrop
    bc = args.bc
    lim = args.lim
    fold_name = 'Processed'
    if PATH is None:
        root = Tk()
        root.withdraw()
        PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Please select the folder with the files to be cropped as square")
        print('Working folder:', PATH)
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
             fold_name = fold_name+'_bc'
    else:
         bc = None    
         
    if ccrp is None:
        q = question('Center crop images?',['Y','y','N','n'])
        if q in ['Y','y']:
            ccrp = q
            fold_name = fold_name+'_crp'
    else:
         ccrp = None   
            
    if res is None:
         q = question('Resize images?',['Y','y','N','n'])
         res = q
         if q in ['Y','y']:
             while True:
                 
                 dim = input('Insert desired cell size in meters to resize images ' )
                 try:    
                     cell_size=int(dim)
                     break
                 except:
                     try:
                         cell_size=float(dim)
                         break
                     except:
                         print('Please enter a valid number')
             fold_name = fold_name+'_res_'+str(cell_size)+'m'
         else:
             dim = None           
    if lim is None:
        q = question('Resize images below a limit?',['Y','y','N','n'])
        lim = q
        if q in ['Y','y']:
            while True:
                
                lim_crp = input('Insert desired size limit images ' )
                try:    
                    limit_size=int(lim_crp)
                    break
                except:
                    try:
                        limit_size=float(lim_crp)
                        break
                    except:
                        print('Please enter a valid number')
            fold_name = fold_name+'_res_'+str(limit_size)+'px'
        else:
            lim_crp = None           
    
    


    if bc == None and ccrp == None and dim == None and lim == None:
        print('Please select at least one task')
    else:
        #dst_folder = make_folder(PATH, fold_name)
        dst_folder = PATH+'/'+fold_name
        os.makedirs(dst_folder, exist_ok=True)
    
        
main()
