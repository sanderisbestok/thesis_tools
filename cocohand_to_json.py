# cochands_to_json.py maakt de coco hands bruikbaar om om te laten zetten naar de verschillende
# formaten voor de netwerken. Coco hands heeft wel extra werk nodig, omdat er geen segementatie
# van de handen is in de cocohands dataset. De cocohands moet dus gecombineerd worden met 
# de segmentatie van de originele coco dataset.
#drie folders, train, test, val

# |-- train
# |  | -- images
# |  | -- annotations.json
# |-- val
# |  | -- images
# |  | -- annotations.json
# |-- test
# |  | -- images
# |  | -- annotations.json

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

# Twee dicts maken eentje met COCO en eentje met COCO Hand

from collections import defaultdict
from pycocotools.coco import COCO
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
pylab.rcParams['figure.figsize'] = (8.0, 10.0)
from PIL import Image
import re
from shapely.geometry import Polygon, mapping
from shapely.geometry import box
import pprint
from shapely.geos import TopologicalError
import os
import shutil
import json
import random

pp = pprint.PrettyPrinter(indent=4)
IMG_SOURCE = '/media/sander/Elements/datasets/raw_data/COCO_Hand_raw/COCO-Hand-Big/COCO-Hand-big_Images'
SAVE_DIR = '/media/sander/Elements/datasets/processed_data/cocohands-s/'
SAVE_FILE = 'annotations.json'

def get_cocohand_annotations():
    annotations = {}
    
    i = 0

    with open('/media/sander/Elements/datasets/raw_data/COCO_Hand_raw/COCO-Hand-Big/COCO-Hand-Big_annotations.txt') as f:
        for line in f:
            data = line.split(",")

            #imgname xmin xmax ymin ymax
            if data[0] in annotations:
                annotations[data[0]].append({"xmin" : int(data[1]), "xmax" : int(data[2]), "ymin": int(data[3]), "ymax" : int(data[4])})
            else:
                annotations[data[0]] = [{"xmin" : int(data[1]), "xmax" : int(data[2]), "ymin" : int(data[3]), "ymax" : int(data[4])}]

            # if i == 100:
            #     break
            # i = i + 1

    return annotations

def get_coco_segmentations(coco_hand_images):
    coco_train=COCO('/media/sander/Elements/datasets/raw_data/coco_annotations/instances_train2014.json')
    coco_val=COCO('/media/sander/Elements/datasets/raw_data/coco_annotations/instances_val2014.json')
    coco_segmentations = {}


    train_ids = []
    val_ids = []

    for image_name in sorted(coco_hand_images):
        train = True
        
        image_id = int(re.findall("[1-9][0-9]*", image_name)[0])

        try:
            img = coco_train.loadImgs(image_id)
            train_ids.append(image_name)
            coco = coco_train
        except:
            img = coco_val.loadImgs(image_id)
            val_ids.append(image_name)
            coco = coco_val

        height = img[0]["height"] 
        width = img[0]["width"]

        # #TMP VOOR TEKENEN
        # name = re.findall("[0-9]*\.jpg", img[0]["file_name"])[0]
        # im = Image.open('/media/sander/Elements/datasets/raw_data/COCO_Hand_raw/COCO-Hand-Big/COCO-Hand-Big_Images/' + name )
        #     # # Create figure and axes
        # fig, ax = plt.subplots()
        # # # Display the image
        # ax.imshow(im)

        annIds = coco.getAnnIds(imgIds=image_id, catIds=1, iscrowd=0)
        anns = coco.loadAnns(annIds)

        for instance in anns:
            for segmentation in instance["segmentation"]:
                segmentation_tuples = []
                for index, _ in enumerate(segmentation):
                    if (index % 2 == 0):
                        segmentation[index] = segmentation[index] / width * 480
                    else:
                        segmentation[index] = segmentation[index] / height * 360
                        segmentation_tuples.append((segmentation[index - 1], segmentation[index]))
                        # plt.scatter([segmentation[index-1]], [segmentation[index]])
                if image_name in coco_segmentations:          
                    coco_segmentations[image_name].append(segmentation_tuples)
                else:
                    coco_segmentations[image_name] = [segmentation_tuples]

    return coco_segmentations, train_ids, val_ids

def get_bboxes(images, cocohand_annotations, coco_segmentations, train_ids, val_ids):
    intersections = {}
    images_to_drop = []

    for image_name in sorted(images):    
        delete = False

        for hand in cocohand_annotations[image_name]:
            hand_bbox = box(hand["xmin"],hand["ymin"],hand["xmax"],hand["ymax"])

            segmentation_match = 0

            for segmentation in coco_segmentations[image_name]:
                full_segmentation = Polygon(segmentation)                        
         
                try:
                    intersection = hand_bbox.intersection(full_segmentation)
                except:    
                    images_to_drop.append(image_name)
                    intersection = False

                if intersection:
                    segmentation_match = segmentation_match + 1

                    if image_name in intersections:
                        intersections[image_name].append(intersection)
                    else:
                        intersections[image_name] = [intersection]
                    
                    if intersection.geom_type != "Polygon":
                        delete = True
            
            
            # een bbox is met meerdere segments gematched of met nul
            if segmentation_match > 1:
                delete = True
            elif segmentation_match == 0:
                delete = True

        if delete:
            images_to_drop.append(image_name)


    # actual images droppen
    for key in images_to_drop:
        if key in intersections:
            del intersections[key]
        if key in train_ids:
            train_ids.remove(key)
        if key in val_ids:
            val_ids.remove(key)


    print(len(train_ids))
    print(len(val_ids))

    return intersections
    


cocohand_annotations = get_cocohand_annotations()

images = cocohand_annotations.keys()

coco_segmentations, train_ids, val_ids = get_coco_segmentations(images)

all_bboxes = get_bboxes(images, cocohand_annotations, coco_segmentations, train_ids, val_ids)

exit()

os.makedirs(os.path.join(SAVE_DIR, "tmp"))
tmp_dir = os.path.join(SAVE_DIR, "tmp")
tmp_img_dir = os.path.join(tmp_dir, "images")

shutil.copytree(IMG_SOURCE, os.path.join(tmp_img_dir))


annotations = {}

for image_name, bboxes in all_bboxes.items():
    image = {
        "name": image_name,
        "objects": []
    }
    
    for bbox in bboxes:
        image["objects"].append(list(bbox.exterior.coords))

    annotations[image_name] = image

with open(os.path.join(tmp_dir, SAVE_FILE), 'w') as output_json_file:
    json.dump(annotations, output_json_file)    


# .json weer inladen, afbeeldingen verplaatsen (nu al gedaan naar cocohands/images)
# splitsen in train/val/test

os.makedirs(os.path.join(SAVE_DIR, "train"))
train_dir = os.path.join(SAVE_DIR, "train")
os.makedirs(os.path.join(train_dir, "images"))

os.makedirs(os.path.join(SAVE_DIR, "val"))
val_dir = os.path.join(SAVE_DIR, "val")
os.makedirs(os.path.join(val_dir, "images"))

os.makedirs(os.path.join(SAVE_DIR, "test"))
test_dir = os.path.join(SAVE_DIR, "test")
os.makedirs(os.path.join(test_dir, "images"))

# Opening JSON file
with open(os.path.join(tmp_dir, 'annotations.json')) as json_file:
    data = json.load(json_file)

    # 0.7
    train_keys = random.sample(list(data), round(len(data) * 0.7))

    train = {k: v for k, v in data.items() if k in train_keys}
    not_train = {k: v for k, v in data.items() if k not in train_keys}

    val_keys = random.sample(list(not_train), round(len(not_train) * 0.5))

    validation = {k: v for k, v in not_train.items() if k in val_keys}
    test = {k: v for k, v in not_train.items() if k not in val_keys}

    for key, _ in train.items():
        shutil.move(os.path.join(tmp_img_dir, key), os.path.join(train_dir, "images", key))

    for key, _ in validation.items():
        shutil.move(os.path.join(tmp_img_dir, key), os.path.join(val_dir, "images", key))

    for key, _ in test.items():
        shutil.move(os.path.join(tmp_img_dir, key), os.path.join(test_dir, "images", key))

    with open(os.path.join(train_dir, SAVE_FILE), 'w') as output_json_file:
        json.dump(train, output_json_file)

    with open(os.path.join(val_dir, SAVE_FILE), 'w') as output_json_file:
        json.dump(validation, output_json_file)

    with open(os.path.join(test_dir, SAVE_FILE), 'w') as output_json_file:
        json.dump(test, output_json_file)


print(len(validation))
print(len(test))
print(len(train))













# loop through images which are in coco_hand


# plt.show()

# check de intersectie tussen bbox en mask

# print(image_name)
# print(segmentation)
# print(cocohand_annotations[image_name])

# elke bbox intersectie met elke segmentatie moet op 1 regel want dat is 1 object voor de coco


# os.makedirs(os.path.join(SAVE_DIR, "tmp"))
# tmp_dir = os.path.join(SAVE_DIR, "tmp")
# img_dir = os.path.join(tmp_dir, "images")

# shutil.copytree(IMG_SOURCE, os.path.join(img_dir))

# for img in 

# annotations = {}
# for dir_name in os.listdir(directory):
#     if not (dir_name == "images"):
#         for _, _, files in os.walk(os.path.join(directory, dir_name)):
#             mat = scipy.io.loadmat(os.path.join(directory, dir_name, ANNOTATION_FILE))

#             for i, img_file in enumerate(sorted(files)):
#                 if not (img_file.endswith(".mat")):
#                     new_img_file = dir_name + "_" + img_file

#                     image = {
#                         "name":     new_img_file,
#                         "objects":  []
#                     }

#                     for segmentation in mat["polygons"][0][i]:
#                         if segmentation.any():
#                             image["objects"].append(segmentation.tolist())
                    
#                     annotations[new_img_file] = image

#                     shutil.move(os.path.join(directory, dir_name, img_file), os.path.join(img_dir, new_img_file))

# with open(os.path.join(directory, SAVE_FILE), 'w') as output_json_file:
#     json.dump(annotations, output_json_file)

# for dir_name in os.listdir(directory):
#     if not (dir_name == "images" or dir_name == "annotations.json"):
#         shutil.rmtree(os.path.join(directory, dir_name))


    
# os.makedirs(os.path.join(SAVE_DIR, "train"))
# train_dir = os.path.join(SAVE_DIR, "train")
# os.makedirs(os.path.join(train_dir, "images"))

# os.makedirs(os.path.join(SAVE_DIR, "val"))
# val_dir = os.path.join(SAVE_DIR, "val")
# os.makedirs(os.path.join(val_dir, "images"))

    # # Opening JSON file
    # with open(os.path.join(tmp_dir, 'annotations.json')) as json_file:
    #     data = json.load(json_file)

    #     # 0.1765 is 15% van 100%
    #     val_keys = random.sample(list(data), round(len(data) * 0.1765))

    #     validation = {k: v for k, v in data.items() if k in val_keys}
    #     train = {k: v for k, v in data.items() if k not in val_keys}

    # with open(os.path.join(val_dir, SAVE_FILE), 'w') as output_json_file:
    #     json.dump(validation, output_json_file)

    # with open(os.path.join(train_dir, SAVE_FILE), 'w') as output_json_file:
    #     json.dump(train, output_json_file)
        
    # for key, _ in validation.items():
    #     shutil.move(os.path.join(tmp_dir, "images", key), os.path.join(val_dir, "images", key))

    # for key, _ in train.items():
    #     shutil.move(os.path.join(tmp_dir, "images", key), os.path.join(train_dir, "images"))

    # shutil.rmtree(tmp_dir)




    







# print(imgIds)
# I = io.imread('/media/sander/Elements/datasets/raw_data/COCO_Hand_raw/COCO-Hand-Big/COCO-Hand-Big_Images/000000000036.jpg')




# print(img)
# I = io.imread(img[0]['coco_url'])



# load and display instance annotations
# plt.imshow(I); plt.axis('off')


# my images are 480*360
# coco official is 640*480

# print(anns)

# # Create figure and axes
# fig, ax = plt.subplots()

# # Display the image
# ax.imshow(im)





# plt.show()

# coco.showAnns(anns)
# plt.show()


