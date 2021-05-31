import os 
import shutil 
import scipy.io
import random
from distutils.dir_util import copy_tree
import csv

# mittel_to_groundtruth.py maakt de hand dataset van Mittel en Zisserman bruikbaar om om te laten zetten
# als test set. Er is slechts een test folder nodig omdat deze dataset niet gebruikt wordt voor
# trainen. De structuur wordt meteen naar de goede groundtruth structuur omgezet.

# |-- test
# |  | -- images
# |  | -- annotations

# annotations.json:
# { 
#     "CARDS_OFFICE_H_T_frame_0001.jpg": 
#     {
#         "name": "CARDS_OFFICE_H_T_frame_0001.jpg",
#         "objects": [[]]
#     },
#     "CARDS_OFFICE_H_T_frame_0002.jpg":
#     {
#         "name": "CARDS_OFFICE_H_T_frame_0002.jpg",
#         "objects": [[]]
#     }
# }

ROOT_DIR = "../"

def make_folders():
    img_dir = os.path.join(ROOT_DIR, "processed_data", "mittel_zisserman", "images")
    annotation_dir = os.path.join(ROOT_DIR, "processed_data", "mittel_zisserman", "annotations")

    # if os.path.exists(img_dir):
    #     shutil.rmtree(img_dir)
    # if os.path.exists(annotation_dir):
    #     shutil.rmtree(annotation_dir)
    # os.makedirs(img_dir)
    # os.makedirs(annotation_dir)

    return img_dir, annotation_dir


raw_images = os.path.join(ROOT_DIR, "raw_data", "mittel_zisserman", "test_dataset", "test_data", "images")
raw_annotation = os.path.join(ROOT_DIR, "raw_data", "mittel_zisserman", "test_dataset", "test_data", "annotations")
img_dir, annotation_dir = make_folders()

# move images to correct folder
# copy_tree(raw_images, img_dir)

for _, _, files in os.walk(raw_annotation):
    for annotation_file in files:
        if (annotation_file.endswith(".mat")):
            mat = scipy.io.loadmat(os.path.join(raw_annotation, annotation_file))

            annotations = []

            for box in mat["boxes"][0]:
                y_coordinates = []
                x_coordinates = []

                y_coordinates.append(box[0][0][0][0][0])
                y_coordinates.append(box[0][0][1][0][0])
                y_coordinates.append(box[0][0][2][0][0])
                y_coordinates.append(box[0][0][3][0][0])

                x_coordinates.append(box[0][0][0][0][1])
                x_coordinates.append(box[0][0][1][0][1])
                x_coordinates.append(box[0][0][2][0][1])
                x_coordinates.append(box[0][0][3][0][1])
                
                x = min(x_coordinates)
                y = min(y_coordinates)
                w = max(x_coordinates) - x
                h = max(y_coordinates) - y
                       
                annotations.append([1, x, y, w, h])

            with open(os.path.join(annotation_dir, annotation_file[:-4]+".txt"),"w+") as my_csv:
                csvWriter = csv.writer(my_csv,delimiter=' ')
                csvWriter.writerows(annotations)
        
