import pickle, math, shutil, tempfile, Image
from os import listdir, mkdir
from os.path import exists, isdir, isfile, join, normpath, basename

from numpy import max, zeros, average, dot, asfarray, sort, trace, argmin
from numpy.linalg import eigh, svd

import os
import sys
import cv2
import numpy as np


def validate_directory(images_list):
    """ Validates images directory, all should be images
    of the same size """
    if not images_list:
        raise IOError, 'Folder empty'

    file_list, sizes = [], set()
    for name in images_list:
        img = Image.open(name).convert('L')
        file_list.append(img)
        sizes.add(img.size)

    if len(sizes) != 1:
        raise IOError, 'Select folder with all images of equal dimensions'
    return file_list


def create_face_bundle(images_list,outdir):
    """ Creates FaceBundle """
    images = validate_directory(images_list)

    img = images[0]
    width, height = img.size
    pixels = width * height
    numimgs = len(images)

    # Create a 2d array, each row holds pixvalues of a single image
    facet_matrix = zeros((numimgs, pixels))
    for i in xrange(numimgs):
        pixels = asfarray(images[i].getdata())
        facet_matrix[i] = pixels / max(pixels)

    # Create average values, one for each column (ie pixel)
    avg = average(facet_matrix, axis=0)
   
        # Create average image in current directory just for fun of viewing
    make_image(avg,outdir, (width, height))


def make_image(v,outdir, size, scaled=True):
#     """ Builds an image named `filename` of `size` dimensions
#     that might be scaled """
     v.shape = (-1,) #change to 1 dim array
     im = Image.new('L', size)
     if scaled:
         a, b = v.min(), v.max()
         v = ((v - a) * 255 / (b - a))
     im.putdata(v)
     im.save(outdir + "/mean.png")


def parse_folder(directory, filter_rule=None):
    """ Returns a list of files in `directory` that complies `filter_rule`.
    Raises IOError if `directory` is not a directory. Returns all files
    in `directory` if no filter rule is passed"""
    return sorted(filter(filter_rule,
                         (normpath(join(directory, name))
                            for name in listdir(directory))))

if __name__ == '__main__':
 
 images_list = parse_folder(sys.argv[1],
                               lambda name: name.lower())
 create_face_bundle(images_list,sys.argv[2]);


