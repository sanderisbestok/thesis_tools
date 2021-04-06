#!/usr/bin/env python3

import datetime
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
import scipy.io
import csv
import random

ROOT_DIR = "../egohands_data"
ANNOTATION_FILE = "polygons.mat"
width = 1280
height = 720

def rename_images():
    # Images need to be renamed, so that they are unique.
    for dir_name in os.listdir(ROOT_DIR):
        for _, _, files in os.walk(os.path.join(ROOT_DIR, dir_name)):
            for file_name in files:
                if not (file_name.endswith(".mat")):
                    new_file_name = dir_name + "_" + file_name
                    os.rename(os.path.join(ROOT_DIR, dir_name, file_name), os.path.join(ROOT_DIR, dir_name, new_file_name))

def remove_parent_folders():
    # Images need to be moved
    for dir_name in os.listdir(ROOT_DIR):
        for _, _, files in os.walk(os.path.join(ROOT_DIR, dir_name)):
            for file_name in files:
                if not (file_name.endswith(".mat")):
                    os.rename(os.path.join(ROOT_DIR, dir_name, file_name), os.path.join(ROOT_DIR, file_name))
                else:
                    os.remove(os.path.join(ROOT_DIR, dir_name, file_name))
        if (os.path.isdir(os.path.join(ROOT_DIR, dir_name))):
            os.rmdir(os.path.join(ROOT_DIR, dir_name))



def generate_coco():  
    object_class = 0

    for dir_name in os.listdir(ROOT_DIR):
        for _, _, files in os.walk(os.path.join(ROOT_DIR, dir_name)):
            mat = scipy.io.loadmat(os.path.join(ROOT_DIR, dir_name, ANNOTATION_FILE))

            for i, img_file in enumerate(sorted(files)):
                if not (img_file.endswith(".mat")):
                    bboxes = []
                    

                    for segmentation in mat["polygons"][0][i]:
                        if segmentation.any():
                            seg_np = np.array(segmentation)

                            min_x = min(seg_np[:,0])
                            max_x = max(seg_np[:,0])
                            min_y = min(seg_np[:,1])
                            max_y = max(seg_np[:,1])

                            box_width = max_x-min_x
                            box_height = max_y-min_y
                            center_x = max_x - (box_width/2)
                            center_y = max_y - (box_height/2)

                            bboxes.append([object_class, center_x, center_y, box_width, box_height])

                    with open(os.path.join(ROOT_DIR, dir_name, img_file[:-4]+".txt"),"w+") as my_csv:
                        csvWriter = csv.writer(my_csv,delimiter=' ')
                        csvWriter.writerows(bboxes)

def split():
    train = 0.15
    val =  0.15
    test = 0.70

    os.makedirs(ROOT_DIR + "/train/labels")
    os.makedirs(ROOT_DIR + "/train/images")
    os.makedirs(ROOT_DIR + "/val/labels")
    os.makedirs(ROOT_DIR + "/val/images")
    os.makedirs(ROOT_DIR + "/test/labels")
    os.makedirs(ROOT_DIR + "/test/images")

    images = []
    annotations = []

    for file in os.listdir(ROOT_DIR):
        if file.endswith(".jpg"):
            images.append(file)
            annotations.append(file[:-4]+".txt")

    ind = list(zip(images, annotations))
    random.shuffle(ind)
    images, annotations = zip(*ind)

    train_images, val_images, test_images = np.split(np.array(images),
                                                          [int(len(images)*0.7), int(len(images)*0.85)])
    train_annotations, val_annotations, test_annotations = np.split(np.array(annotations),
                                                          [int(len(annotations)*0.7), int(len(annotations)*0.85)])

    for name in train_images:
        os.rename(os.path.join(ROOT_DIR, name), os.path.join(ROOT_DIR, "train/images", name))

    for name in train_annotations:
        os.rename(os.path.join(ROOT_DIR, name), os.path.join(ROOT_DIR, "train/labels", name))

    for name in val_images:
        os.rename(os.path.join(ROOT_DIR, name), os.path.join(ROOT_DIR, "val/images", name))

    for name in val_annotations:
        os.rename(os.path.join(ROOT_DIR, name), os.path.join(ROOT_DIR, "val/labels", name))

    for name in test_images:
        os.rename(os.path.join(ROOT_DIR, name), os.path.join(ROOT_DIR, "test/images", name))

    for name in test_annotations:
        os.rename(os.path.join(ROOT_DIR, name), os.path.join(ROOT_DIR, "test/labels", name))
                          

# rename_images()
# generate_coco()
# remove_parent_folders()
split()

