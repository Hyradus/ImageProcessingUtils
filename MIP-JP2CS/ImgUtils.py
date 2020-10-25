#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Sun Oct 25 14:49:26 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
import rasterio as rio


def GTiffWriter(save_name, img, img_crs, tile_transform):
    with rio.open(save_name, 'w',
                              driver = 'GTiff',
                              height= img.shape[0],
                              width=img.shape[1],
                              count=1,
                              dtype=img.dtype,
                              crs=img_crs,
                              transform=tile_transform) as dst:
                    dst.write(img, 1)    