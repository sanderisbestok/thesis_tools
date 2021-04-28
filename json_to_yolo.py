import os
import json
import numpy as np
import csv

ROOT_DIR = "../data"

def create_folders():
    os.makedirs(os.path.join(ROOT_DIR, "yolo"))
    os.makedirs(os.path.join(ROOT_DIR, "yolo", "train"))
    os.makedirs(os.path.join(ROOT_DIR, "yolo", "val"))
    os.makedirs(os.path.join(ROOT_DIR, "yolo", "test"))
    os.makedirs(os.path.join(ROOT_DIR, "yolo", "train", "labels"))
    os.makedirs(os.path.join(ROOT_DIR, "yolo", "val", "labels"))
    os.makedirs(os.path.join(ROOT_DIR, "yolo", "test", "labels"))

    os.symlink("../../json/train/images", os.path.join(ROOT_DIR, "yolo", "train", "images"))
    os.symlink("../../json/val/images", os.path.join(ROOT_DIR, "yolo", "val", "images"))
    os.symlink("../../json/test/images", os.path.join(ROOT_DIR, "yolo", "test", "images"))

def create_annotations():
    object_class = 0

    for dir_name in os.listdir(os.path.join(ROOT_DIR, "json")):
        with open(os.path.join(ROOT_DIR, "json", dir_name, 'annotations.json')) as json_file:
            data = json.load(json_file)

            for key, value in data.items():
                bboxes = []              

                for segmentation in value["objects"]:
                    seg_np = np.array(segmentation)
                
                    min_x = min(seg_np[:,0]) / 1280
                    max_x = max(seg_np[:,0]) / 1280
                    min_y = min(seg_np[:,1]) / 720
                    max_y = max(seg_np[:,1]) / 720

                    box_width = (max_x-min_x)
                    box_height = (max_y-min_y)
                    center_x = (max_x - (box_width/2))
                    center_y = (max_y - (box_height/2))

                    bboxes.append([object_class, center_x, center_y, box_width, box_height])

                with open(os.path.join(ROOT_DIR, "yolo", dir_name, "labels", key[:-4]+".txt"),"w+") as my_csv:
                    csvWriter = csv.writer(my_csv,delimiter=' ')
                    csvWriter.writerows(bboxes)



create_folders()
create_annotations()