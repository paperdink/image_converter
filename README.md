# Image converter tool

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [ImageMagick](https://imagemagick.org/script/download.php)
- Install python dependencies `pip install -r requirements.txt`


## Usage
```
usage: img_conv.py [-h] --dev b --path p [--dither d] [--dither_diffusion f]

Generate images to display on paperd.ink

options:
  -h, --help            show this help message and exit
  --dev b               paperd.ink device
  --path p              path of the image file
  --dither d            dither setting to use (default: FloydSteinberg)
  --dither_diffusion f  diffusion amount (default: 85)
```
