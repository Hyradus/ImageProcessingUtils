# ImageProcessingUtils
[![DOI](https://zenodo.org/badge/287286230.svg)](https://zenodo.org/badge/latestdoi/287286230)

Author: giacomo.nodjoumi@hyranet.info - g.nodjoumi@jacobs-university.de

ImageProcessingUtils is a Jupyter Notebook for processing georeferenced images such as GeoTiff, JP2, png/jpeg+world file, CUB (USGS ISIS).
With this tool is possible to perform single to multiple tasks including:

* convert to GeoTiff, Cloud Optimize GeoTiff (COG), JP2, png/jpeg+world file, CUB (USGS ISIS)
* rescale images pixel resolution
* create tiles for images larger than user-defined size limit
* remove black borders for images/tiles
* crop images/tiles with a 1:1 centered aspect ration

The notebook is served through a docker image containing all required packages.

This study is within the Europlanet 2024 RI and EXPLORE project, and it has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 871149 and No 101004214.

_____________________________________________________________________________

## Requirements

Docker
Linux OS (dockerfile should work also on Windows and MacOS)

## Installation

To build the image in Linux environment run:
```
sudo chmod +x ImageBuilder.sh
./ImageBuilder.sh
```

## Usage

```
docker run -it --rm --name ipu -e NB_UID=$UID -e NB_GID=$GID -e CHOWN_HOME=yes -e CHOWN_EXTRA_OPTS='-R'  -p custom_port:8888 -v path-to-data:/data ipu:lab
```

### User permission consistency
To have consistency between the host and docker users permissions, is suggested to user in docker run those additional environmental parameters
```
NB_UID=$UID
NB_GID=$GID
CHOWN_HOME=yes
CHOWN_EXTRA_OPTS='-R'
```
Then edit the general configuration dictionary in cell n°3.

```
config = {
'PATH':"../data/",
'DST_PATH':"../data/",
'IXT':'cub',
'OXT':'tiff',
'BC':'n',
'SQCRP':'n',
'RES':'y',
'CELL_SIZE':'2',
'LIM':'n',
'LIM_SIZE':None,
'COG':'y',
'8bit':'y',
'dem':'n'
}
```
**PATH and DST_PATH must be edited if the data is contained in subfolders**
**other parameters, if not set here, will be asked interactively**
**dem is a flag to avoid JPEG compression and 8bit conversion when source image is a DEM
### Cloud Optimized Geotiff

Additional configuration is required for creating COG files in [COG Config](#COG_Config).
```
cog_cfg = {
    'COMPRESS':'JPEG',
    'RESAMPLING':'NEAREST',
    #'JPEG_QUALITY=90',
    #'PHOTOMETRIC=YCBCR',
    'TILED':'YES',
    'BLOCKXSIZE':'512',
    'BLOCKYSIZE':'512',
    'BIGTIFF':'IF_NEEDED',
    'ALPHA':'YES',
    'levels':[2,4,8,16,32,64]
}
```

## Acknowledgment
This work is within the Europlanet 2024 RI and EXPLORE project, and it has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 871149 and No 101004214.
