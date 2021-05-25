#!/usr/bin/env python3

import datetime
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
import scipy.io
from pycococreatortools import pycococreatortools

ROOT_DIR = "../egohands_coco"
ANNOTATION_FILE = "polygons.mat"
SAVE_FILE = "annotations.json"

INFO = {
    "description": "EgoHands",
    "url": "http://vision.soic.indiana.edu/projects/egohands/",
    "version": "1.0",
    "year": 2015,
    "contributor": "Bambach, Sven and Lee, Stefan and Crandall, David J. and Yu, Chen",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'hand',
        'supercategory': 'hand',
    },
]

coco_output = {
    "info": INFO,
    "licenses": LICENSES,
    "categories": CATEGORIES,
    "images": [],
    "annotations": []
}

def rename_images():
    # Images need to be renamed, so that they are unique.
    for dir_name in os.listdir(ROOT_DIR):
        for _, _, files in os.walk(os.path.join(ROOT_DIR, dir_name)):
            for file_name in files:
                if not (file_name.endswith(".mat")):
                    new_file_name = dir_name + "_" + file_name
                    os.rename(os.path.join(ROOT_DIR, dir_name, file_name), os.path.join(ROOT_DIR, dir_name, new_file_name))

def remove_parent_folders():
    # Images need to be renamed, so that they are unique.
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
    image_id = 1
    segmentation_id = 1
    category_info = {'id': 1, 'is_crowd': 0}

    for dir_name in os.listdir(ROOT_DIR):
        for _, _, files in os.walk(os.path.join(ROOT_DIR, dir_name)):
            mat = scipy.io.loadmat(os.path.join(ROOT_DIR, dir_name, ANNOTATION_FILE))

            for i, img_file in enumerate(sorted(files)):
                if not (img_file.endswith(".mat")):
                    image = Image.open(os.path.join(ROOT_DIR, dir_name, img_file))
                    image_info = pycococreatortools.create_image_info(image_id, os.path.basename(img_file), image.size)
                    
                    coco_output["images"].append(image_info)

                    for segmentation in mat["polygons"][0][i]:
                        if segmentation.any():
                            seg_np = np.array(segmentation)

                            min_x = min(seg_np[:,0])
                            max_x = max(seg_np[:,0])
                            min_y = min(seg_np[:,1])
                            max_y = max(seg_np[:,1])

                            bbox = [min_x,min_y, max_x-min_x,max_y-min_y]
                            

                            annotation_info = {
                                "id": segmentation_id,
                                "image_id": image_id,
                                "category_id": 1,
                                "iscrowd": 0,
                            #     "area": area.tolist(),
                                "bbox": bbox,
                                "segmentation": [[val for sublist in segmentation for val in sublist]],
                                "width": image.size[0],
                                "height": image.size[1],
                            } 

                            # kijken of we hiermee polygons kunnen mkaen
                            coco_output["annotations"].append(annotation_info)
                            # print(coco_output)
                            

                        segmentation_id += 1
                    
                    image_id = image_id + 1

    with open(os.path.join(ROOT_DIR, SAVE_FILE), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


rename_images()
# generate_coco()
remove_parent_folders()
