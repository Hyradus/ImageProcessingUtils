# ImageProcessingUtils
[![DOI](https://zenodo.org/badge/287286230.svg)](https://zenodo.org/badge/latestdoi/287286230)


This repo contain image processing utilities that i used for prepare images before Deep Learning training
   
_____________________________________________________________________________

# MIP-SCR - Multi Image Parallel Square Crop Resize
This script do:

- Crop images to 1:1 aspect ratio from the center of the image
- Remove black borders from image
- Resize cell-size of image to user-defined size
- Create tiles if images are above a user-defined limit
- Convert from JP2 format to Ge

It also attempt, if requested by user, to adapt vertical and horizontal tiles 
number to return tiles with almost 1:1 aspect ratio. (TO BE imrpooved)

## Usage
- Create provided environment or install required packages
- Just execute the script and interactively insert all parameters.
If using CLI execute the script passing at least --PATH argument

The script will automatically create subfolders containing the results. 

