from PIL import Image
#import matplotlib.pyplot as plt
#import numpy as np
import subprocess
import argparse
import os
import logging

TEMP_FILE_PATH = '/tmp/paperd_ink_output.bmp'

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Argument parser configuration
parser = argparse.ArgumentParser(description='Process images to display on paperd.ink')

parser.add_argument('output_type', type=str, choices=['header', 'bitmap'],
                    help='Output C header or bitmap format')
parser.add_argument('--dev', dest='device', metavar='b', type=str, required=True, choices=['classic', 'merlot'],
                    help='paperd.ink device')
parser.add_argument('--path', dest='image_path', metavar='p', type=str, required=True,
                    help='path of the image file')
parser.add_argument('--dither', dest='dither', metavar='d', type=str, choices=['FloydSteinberg'],
                    default='FloydSteinberg',
                    help='dither setting to use (default: FloydSteinberg)')
parser.add_argument('--dither_diffusion', dest='diffusion', metavar='f', type=int, choices=range(0,100),
                    default=85,
                    help='diffusion amount (default: 85)')

args = parser.parse_args()

logging.info("Processing for paperd.ink {0}".format(args.device))

# Create bitmap from input image
image_name = os.path.basename(args.image_path).split('.')[0]
logging.info("Processing {0}".format(image_name))

subprocess.run(['rm', '-rf', TEMP_FILE_PATH])
remap = '{0}.png'.format(args.device)

subprocess.check_call(['convert', args.image_path, '-dither', args.dither, '-define', 'dither:diffusion-amount={0}%'.format(args.diffusion),
                        '-remap', remap, 'BMP3:{0}'.format(TEMP_FILE_PATH)])

logging.info("Outputing {0}".format(args.output_type))

if args.output_type == 'bitmap':    
    subprocess.check_call(['cp', TEMP_FILE_PATH, "{0}.bmp".format(image_name)])
    logging.info("Successfully generated {0}.bmp file".format(image_name))
    exit(0)

image = Image.open(TEMP_FILE_PATH)

if image.width > 400 or image.height > 300:
    logging.error("Please resize image to 400x300 px")
    exit(-1)

exp_byte_count = int(image.width/8)*image.height

# Extract image data and create header file
# While displaying on e-paper we send a black image
# and a red image (in case of 3-color-epaper)
img_data = []
img_black_bytes = [] # list of black image bytes
img_red_bytes = [] # list of red image bytes
black_byte = 0
red_byte = 0
for i,bit in enumerate(image.tobytes()):
    img_data.append(bit)
    bit_pos = 7-(i%8) # Bit order to MSB first
    if(bit == 0x02):
        black_byte |= (0 << bit_pos)
        red_byte |= (0 << bit_pos) 
    elif(bit == 0x01):
        black_byte |= (1 << bit_pos)
        red_byte |= (1 << bit_pos)
    else:
        black_byte |= (1 << bit_pos)
        red_byte |= (0 << bit_pos)

    # When the byte is formed with 8 bits
    # Save it in the list
    if i%8 == 7 :
        img_black_bytes.append(black_byte)
        img_red_bytes.append(red_byte)
        black_byte = 0
        red_byte = 0

# Sanity check
if exp_byte_count != len(img_black_bytes):
    logging.info("Byte Count: {0} Exp Byte Count: {1}".format(len(img_black_bytes), exp_byte_count))
    logging.error("Expected byte count and byte count not equal.")
    exit(-1)

# Write data to C header file
with open('{0}.h'.format(image_name), 'w') as output:
    output.write("const unsigned char {0}[{1}] = {{".format(image_name, exp_byte_count))
    for i,byte in enumerate(img_black_bytes):
        if i%16 == 0:
            output.write("\n")
        output.write(" 0x{0:0{1}X},".format(byte, 2))
    output.write("};\n")

    if args.device == 'merlot':
        output.write("const unsigned char {0}_red[{1}] = {{".format(image_name, exp_byte_count))
        for i,byte in enumerate(img_red_bytes):
            if i%16 == 0:
                output.write("\n")
            output.write(" 0x{0:0{1}X},".format(byte, 2))
        output.write("};\n")
    
    output.close()

logging.info("Successfully generated {0}.h file".format(image_name))

# Optionally display the output image
#img_array = np.array(img_data)
#img_array = img_array.reshape((image.height, image.width))
#plt.imshow(img_array, cmap='Greys_r')
#plt.show()