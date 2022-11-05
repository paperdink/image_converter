# Image converter tool

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [ImageMagick](https://imagemagick.org/script/download.php)
- Install python dependencies `pip install -r requirements.txt`


## Usage
```
usage: img_conv.py [-h] --dev b --path p [--dither d] [--diffusion f]

Generate images to display on paperd.ink

options:
  -h, --help     show this help message and exit
  --dev b        paperd.ink device
  --path p       path of the image file
  --dither d     dither setting to use [FloydSteinberg (default), Riemersma, None]
  --diffusion f  diffusion percentage [0 to 100, default=85]
```

A higer diffusion amount creates dotty images while a lower value loses details. 

Set dither to 'None' to get sharper images.
