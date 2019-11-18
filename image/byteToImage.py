# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import os
import numpy as np
import array
import zlib
import

from math import ceil, sqrt
from PIL import Image

# +
#### Configuration

bytes_dir = '../byteFiles'
images_dir = './images'
undecodedByte = 'FF'

try:
    os.makedirs(images_dir)
except FileExistsError:
    pass

concat_path = lambda *args: '/'.join(args)


# -

def findByteFiles():
    dataFiles = os.listdir(bytes_dir)
    dataFiles = list(filter(lambda x: x.endswith('.exe'), dataFiles))
    return dataFiles


# +
def deflate_compressed_size(bytes_in):
    bytes_out = zlib.compress(bytes_in)
    return len(bytes_out)

def deflate_compression_ratio(bytes_in):
    len_out = deflate_compressed_size(bytes_in)
    return (100-len_out/len(bytes_in)*100), len_out


# +
def bytes2png(f, width):
    file = concat_path(bytes_dir, f)
    

    image_name = concat_path(images_dir, f.split('.')[0] + '.png')
#     if os.path.isfile(image_name):
#         print('Image already exists: {}'.format(image_name))
#         return
    
    with open(file,'rb') as f:
        bytes = bytearray(f.read())
        flatNpArray = np.array(bytes)
        
        fileSize = flatNpArray.size
        hight = int(fileSize/width) + 1
        imageSize = (width,hight)
        needToAddElements = width * hight
        print(fileSize)
        print(needToAddElements)
        print(needToAddElements - fileSize)
        pad_width = (0,needToAddElements - fileSize)
        np.pad(flatNpArray,pad_width,'constant')
        print(type(flatNpArray))
        
        grayImage = flatNpArray.resize(hight,width)
        
        pilout = Image.fromarray(np.uint8(flatNpArray))
        pilout.save(image_name)



# +
def main():    
    files = findByteFiles()

    for file in files:
        # Nataraj et al. file size to width table 
    #     images_dir = '.\\imageData_nataraj'
        bytes_file = concat_path(bytes_dir, file)

        with open(bytes_file, 'rb') as f:
            lines = f.read().splitlines()

            file_size=os.path.getsize(bytes_file)
            print('{}: {}kB'.format(file, file_size / 1024))
            if (file_size < 10 * 1024):
                bytes2png(file, 32)
            elif (file_size < 30 * 1024):
                bytes2png(file, 64)
            elif (file_size < 60 * 1024):
                bytes2png(file, 128)
            elif (file_size < 100 * 1024):
                bytes2png(file, 256)
            elif (file_size < 200 * 1024):
                bytes2png(file, 384)
            elif (file_size < 500 * 1024):
                bytes2png(file, 512)
            elif (file_size < 1000 * 1024):
                bytes2png(file, 768)
            else:
                bytes2png(file, 1024)

main()
# -



