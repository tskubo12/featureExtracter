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
#     display_name: syusiML
#     language: python
#     name: syusiml
# ---

# +
import os
import subprocess
import numpy as np
import array
import zlib
import gist
import cv2
import pickle
import sys

from math import ceil, sqrt
from PIL import Image


# -

def bytes2png(file, width):

    with open(file,'rb') as f:
        bytes = bytearray(f.read())
        flatNpArray = np.array(bytes)
        
        fileSize = flatNpArray.size
        hight = int(fileSize/width) + 1
        imageSize = (width,hight)
        needToAddElements = width * hight

        pad_width = (0,needToAddElements - fileSize)
        np.pad(flatNpArray,pad_width,'constant')
        
        flatNpArray.resize(hight,width)
        
        rgbImag = cv2.cvtColor(flatNpArray,cv2.COLOR_GRAY2RGB)
        descriptor = gist.extract(rgbImag)
        return descriptor
    


# ディレクトリの生成
def makeDir(dirName):
    try:
        if(not(os.path.exists(dirName))):
            mkdirArg = ['mkdir',dirName]
            subprocess.check_call(mkdirArg)
        else:
             print(' {} already exists'.format(dirName))
    except:
        sys.exit('can\'t make directory')


def writePickle(obj,filePath):
    try:
        with open(filePath,'wb') as f : 
            pickle.dump(obj,f)
        print('writing {} success'.format(filePath))
    except:
        print('failed writing {}'.format(filePath))


# +
def main():    

    bytes_dir = sys.argv[1]
    undecodedByte = 'FF'
    resultDir = 'results/'
    outPutDir = 'results/imageFeature/'
    
    for dir in [resultDir,outPutDir]:
        makeDir(dir)
    
    for dirpath,dirnames,filenames in os.walk(bytes_dir):
#         bytes_file = concat_path(bytes_dir, file)
        for filename in filenames:
            filePath = dirpath + '/' + filename
            with open(filePath, 'rb') as f:
                lines = f.read().splitlines()

                file_size=os.path.getsize(filePath)
                print('{}: {}kB'.format(filename, file_size / 1024))
                try:
                    if (file_size < 10 * 1024):
                        feature = bytes2png(filePath, 32)
                    elif (file_size < 30 * 1024):
                        feature = bytes2png(filePath, 64)
                    elif (file_size < 60 * 1024):
                        feature = bytes2png(filePath, 128)
                    elif (file_size < 100 * 1024):
                        feature = bytes2png(filePath, 256)
                    elif (file_size < 200 * 1024):
                        feature = bytes2png(filePath, 384)
                    elif (file_size < 500 * 1024):
                        feature = bytes2png(filePath, 512)
                    elif (file_size < 1000 * 1024):
                        feature = bytes2png(filePath, 768)
                    else:
                        feature = bytes2png(filePath, 1024)
                except:
                    print('can not extract {}'.format(filename))
                                
                writePickle(feature,outPutDir + os.path.splitext(filename)[0] + '.pickle')

                
#                 writePickle(feature,outPutDir + filename)

main()
# -

