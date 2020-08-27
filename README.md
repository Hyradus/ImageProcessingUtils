# ImageProcessingUtils

This repo contain image processing utilities that i used for prepare images before Deep Learning training

## MIP-S - Multi Image Parallel Slicer

This script simply divide all images of a folder in a number of vertical and
horizontal tiles provided by user.

It also attempt, if requested by user, to adapt vertical and horizontal tiles 
number to return tiles with almost 1:1 aspect ratio. (TO BE imrpooved)

### Usage

Can be user both using argument parser or interactively 

Valid arguments:

--PATH = path to folder with images
--vt = Number of vertical tiles (integer)
--ht = Number of horizontal tiles (integer)
-art = Flag for trying to adapt tiles to 1:1 aspect ratio (Y/y or N/n)

The script will automatically create subfolders containing the results. BE SURE TO REMOVE THOSE FOLDER BEFORE RUNNING THE SCRIPT AGAIN IN THE SAME MAIN PATH

## MIP-BR - Multi Image Parallel Background Remover

This script try to crop images that have black background borders into rectangular
images with no borders. (TO BE improoved)

### Usage

Can be user both using argument parser or interactively 

Valid arguments:

--PATH = path to folder with images.

The script will automatically create subfolders containing the results. BE SURE TO REMOVE THOSE FOLDER BEFORE RUNNING THE SCRIPT AGAIN IN THE SAME MAIN PATH

## MIP-SR - Multi Image Paraller Square Resizer

This script resize with center cut images to a 1:1 ratio.

If requested by user, it also resize all images to 900x900 pixels

### Usage

Can be user both using argument parser or interactively 

Valid arguments:

--PATH = path to folder with images
--res = Flag for resize all images to 900x900 pixels (Y/y or N/n)

The script will automatically create subfolders containing the results. BE SURE TO REMOVE THOSE FOLDER BEFORE RUNNING THE SCRIPT AGAIN IN THE SAME MAIN PATH
