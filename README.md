# ImageProcessingUtils
[![DOI](https://zenodo.org/badge/287286230.svg)](https://zenodo.org/badge/latestdoi/287286230)


This repo contain image processing utilities that i used for prepare images before Deep Learning training
   
_____________________________________________________________________________

# MIP-S - Multi Image Parallel Slicer

This script simply divide all images of a folder in a number of vertical and
horizontal tiles provided by user.

It also attempt, if requested by user, to adapt vertical and horizontal tiles 
number to return tiles with almost 1:1 aspect ratio. (TO BE imrpooved)

## Usage

Can be user both using argument parser or interactively 

Valid arguments:

* --PATH = path to folder with images
*--vt = Number of vertical tiles (integer)
* --ht = Number of horizontal tiles (integer)
*--art = Flag for trying to adapt tiles to 1:1 aspect ratio (Y/y or N/n)
* --ixt= input file format
* --oxt= output file format

The script will automatically create subfolders containing the results. 

_____________________________________________________________________________
# MIP-BC - Multi Image Parallel Background Cropper

This script try to crop images that have black background borders into rectangular
images with no borders. (TO BE improoved)

## Usage

Can be user both using argument parser or interactively 

Valid arguments:

* --PATH = path to folder with images.
* --ixt= input file format
* --oxt= output file format

The script will automatically create subfolders containing the results. BE SURE TO REMOVE THOSE FOLDER BEFORE RUNNING THE SCRIPT AGAIN IN THE SAME MAIN PATH
_____________________________________________________________________________
# MIP-SR - Multi Image Paraller Square Resizer

This script resize with center cut images to a 1:1 ratio.

If requested by user, it also resize all images to 900x900 pixels

## Usage

Can be user both using argument parser or interactively 

Valid arguments:

* --PATH = path to folder with images
* --res = Flag for resize all images to 900x900 pixels (Y/y or N/n)
* --ixt= input file format
* --oxt= output file format
The script will automatically create subfolders containing the results. BE SURE TO REMOVE THOSE FOLDER BEFORE RUNNING THE SCRIPT AGAIN IN THE SAME MAIN PATH

_____________________________________________________________________________
# MIP-MFR - Multi Image Paraller Mirror Flip Rotate

Script to mirror, flip and rotate given images

## Usage

Can be user both using argument parser or interactively 

Valid arguments:

--PATH = path to folder with images
--m = mirror
--f = flip
--r = rotate 90 and 270
--ixt= input file format
--oxt= output file format

The script will automatically create subfolders containing the results. BE SURE TO REMOVE THOSE FOLDER BEFORE RUNNING THE SCRIPT AGAIN IN THE SAME MAIN PATH

_____________________________________________________________________________
# MIP-SR - Multi Image Paraller Square Resizer

This script resize with center cut images to a 1:1 ratio.

If requested by user, it also resize all images to 900x900 pixels

## Usage

Can be user both using argument parser or interactively 

Valid arguments:

--PATH = path to folder with images
--res = Flag for resize all images to 900x900 pixels (Y/y or N/n)
--ixt= input file format
--oxt= output file format
The script will automatically create subfolders containing the results. BE SURE TO REMOVE THOSE FOLDER BEFORE RUNNING THE SCRIPT AGAIN IN THE SAME MAIN PATH

_____________________________________________________________________________
# MIP-JP2CS - Multi Image Paraller JP2 Converter and Slicer
This script use rasterio to load JP2 images and opencv convert into tiff/png/jpg of a given resolution, saving also a world reference file.

Compatible with Tiff, PNG, JPG

## Usage

Can be user both using argument parser or interactively 

Valid arguments:

* --PATH = path to folder with images
* --sli = flag to select slicing
* --mode = slicing method: D for dimension (e.g. height pixel value of tiles), T for tile numbers (e.g. 5, for 5 vertical tiles. horizontal tiles number will be computed automatically, trying to maintain 1:1 aspect ratio of tiles.
* --t number of tiles
* --dim dimension of tile height

The script will automatically create subfolders containing the results. 
