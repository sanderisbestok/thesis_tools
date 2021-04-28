import os
import json
import numpy as np
import csv

ROOT_DIR = "../data"

def create_folders():
    os.makedirs(os.path.join(ROOT_DIR, "groundtruth"))
    os.makedirs(os.path.join(ROOT_DIR, "groundtruth", "train"))
    os.makedirs(os.path.join(ROOT_DIR, "groundtruth", "val"))
    os.makedirs(os.path.join(ROOT_DIR, "groundtruth", "test"))


def create_annotations():
    object_class = 1

    for dir_name in os.listdir(os.path.join(ROOT_DIR, "json")):
        with open(os.path.join(ROOT_DIR, "json", dir_name, 'annotations.json')) as json_file:
            data = json.load(json_file)

            for key, value in data.items():
                bboxes = []              

                for segmentation in value["objects"]:
                    seg_np = np.array(segmentation)
                
                    min_x = min(seg_np[:,0])
                    max_x = max(seg_np[:,0])
                    min_y = min(seg_np[:,1])
                    max_y = max(seg_np[:,1])

                    box_width = (max_x-min_x)
                    box_height = (max_y-min_y)

                    bboxes.append([object_class, min_x, min_y, box_width, box_height])

                with open(os.path.join(ROOT_DIR, "groundtruth", dir_name, key[:-4]+".txt"),"w+") as my_csv:
                    csvWriter = csv.writer(my_csv,delimiter=' ')
                    csvWriter.writerows(bboxes)



create_folders()
create_annotations()