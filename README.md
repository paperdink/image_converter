# Image converter tool

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [ImageMagick](https://imagemagick.org/script/download.php)

## Usage
```
usage: img_conv.py [-h] --dev b --path p [--dither d] [--dither_diffusion f] {header,bitmap}

Process images to display on paperd.ink

positional arguments:
  {header,bitmap}       Output C header or bitmap format

options:
  -h, --help            show this help message and exit
  --dev b               paperd.ink device
  --path p              path of the image file
  --dither d            dither setting to use (default: FloydSteinberg)
  --dither_diffusion f  diffusion amount (default: 85)
```
