import json
import os
import datetime
from pycococreatortools import pycococreatortools
from PIL import Image
import numpy as np

ROOT_DIR = "../data"
ANNOTATION_FILE = "annotations.json"

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

def create_folders():
    os.makedirs(os.path.join(ROOT_DIR, "extremenet"))
    os.makedirs(os.path.join(ROOT_DIR, "extremenet", "annotations"))
    os.makedirs(os.path.join(ROOT_DIR, "extremenet", "images"))
    os.symlink("../../json/train/images", os.path.join(ROOT_DIR, "extremenet", "images", "train"))
    os.symlink("../../json/val/images", os.path.join(ROOT_DIR, "extremenet", "images", "val"))
    os.symlink("../../json/test/images", os.path.join(ROOT_DIR, "extremenet", "images", "test"))

def create_annotations():
    segmentation_id = 1
    category_info = {'id': 1, 'is_crowd': 0}

    for dir_name in os.listdir(os.path.join(ROOT_DIR, "json")):
        with open(os.path.join(ROOT_DIR, "json", dir_name, 'annotations.json')) as json_file:
            data = json.load(json_file)

            for key, value in data.items():
                image = Image.open(os.path.join(ROOT_DIR, "extremenet", "images", dir_name, key))
                image_info = pycococreatortools.create_image_info(image_id, key, image.size)

                coco_output["images"].append(image_info)

                for segmentation in value["objects"]:
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

                    coco_output["annotations"].append(annotation_info)
                
                    segmentation_id += 1
                    
                image_id = image_id + 1

        with open(os.path.join(ROOT_DIR, "extremenet", "annotations", "annotations_" + dir_name + ".json"), 'w') as output_json_file:
            json.dump(coco_output, output_json_file)



    return



# create_folders()
create_annotations()