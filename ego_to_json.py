import os 
import shutil 
import json
import scipy.io
import random

# ego_to_json.py maakt egohands_data bruikbaar om om te laten zetten naar de verschillende
# formaten voor de netwerken.
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


# In de json staat: 

# {
#   "annotations": [
#     {
#         "file_name": "img_01",
#         "segmentation": segmentations
#     },
#     {
#       "file_name": "img_02",
      
# deze json kan dan gemakkelijk worden omgezet naar het desbetreffende algoritme.
# echter deze json zo simpel mogelijk houden, want deze moet voor elke dataset opnieuw gebouwd worden
# alle info die via omweg uit de json gehaald kan worden, zorgen dat deze in de losse files eruit wordt gehaald.
# dus de alle hele segmentations erin, hier kunnen immers de bboxes uitgehaald worden. (loop per file over alle segmentations heen
# ) De folders kunnen symlinks hebben naar de images in hun eigen structuur.

ROOT_DIR = "../egohands_data"
ANNOTATION_FILE = "polygons.mat"
SAVE_FILE = "annotations.json"


def split_test():
    os.makedirs(os.path.join(ROOT_DIR, "test"))
    
    shutil.move(os.path.join(ROOT_DIR, "CARDS_OFFICE_B_S"), os.path.join(ROOT_DIR, "test", "CARDS_OFFICE_B_S"))
    shutil.move(os.path.join(ROOT_DIR, "CARDS_OFFICE_H_T"), os.path.join(ROOT_DIR, "test", "CARDS_OFFICE_H_T"))
    shutil.move(os.path.join(ROOT_DIR, "CARDS_OFFICE_S_B"), os.path.join(ROOT_DIR, "test", "CARDS_OFFICE_S_B"))
    shutil.move(os.path.join(ROOT_DIR, "CARDS_OFFICE_T_H"), os.path.join(ROOT_DIR, "test", "CARDS_OFFICE_T_H"))
    shutil.move(os.path.join(ROOT_DIR, "PUZZLE_COURTYARD_B_S"), os.path.join(ROOT_DIR, "test", "PUZZLE_COURTYARD_B_S"))
    shutil.move(os.path.join(ROOT_DIR, "PUZZLE_COURTYARD_H_T"), os.path.join(ROOT_DIR, "test", "PUZZLE_COURTYARD_H_T"))
    shutil.move(os.path.join(ROOT_DIR, "PUZZLE_COURTYARD_S_B"), os.path.join(ROOT_DIR, "test", "PUZZLE_COURTYARD_S_B"))

def json_test():
    test_dir = os.path.join(ROOT_DIR, "test")
    os.makedirs(os.path.join(test_dir, "images"))
    img_dir = os.path.join(test_dir, "images")

    create_annotations(test_dir,img_dir)

   
def json_train_val():
    os.makedirs(os.path.join(ROOT_DIR, "tmp"))
    tmp_dir = os.path.join(ROOT_DIR, "tmp")
    os.makedirs(os.path.join(tmp_dir, "images"))
    img_dir = os.path.join(tmp_dir, "images")

    for dir_name in os.listdir(ROOT_DIR):
        if not (dir_name == "tmp" or dir_name == "test"):
            shutil.move(os.path.join(ROOT_DIR, dir_name), os.path.join(ROOT_DIR, tmp_dir, dir_name))

    create_annotations(tmp_dir, img_dir)

def create_annotations(directory, img_dir):
    annotations = {}
    for dir_name in os.listdir(directory):
        if not (dir_name == "images"):
            for _, _, files in os.walk(os.path.join(directory, dir_name)):
                mat = scipy.io.loadmat(os.path.join(directory, dir_name, ANNOTATION_FILE))

                for i, img_file in enumerate(sorted(files)):
                    if not (img_file.endswith(".mat")):
                        new_img_file = dir_name + "_" + img_file

                        image = {
                            "name":     new_img_file,
                            "objects":  []
                        }

                        for segmentation in mat["polygons"][0][i]:
                            if segmentation.any():
                                image["objects"].append(segmentation.tolist())
                        
                        annotations[new_img_file] = image

                        shutil.move(os.path.join(directory, dir_name, img_file), os.path.join(img_dir, new_img_file))

    with open(os.path.join(directory, SAVE_FILE), 'w') as output_json_file:
        json.dump(annotations, output_json_file)

    for dir_name in os.listdir(directory):
        if not (dir_name == "images" or dir_name == "annotations.json"):
            shutil.rmtree(os.path.join(directory, dir_name))

def split_train_val():    
    tmp_dir = os.path.join(ROOT_DIR, "tmp")
    
    os.makedirs(os.path.join(ROOT_DIR, "train"))
    train_dir = os.path.join(ROOT_DIR, "train")
    os.makedirs(os.path.join(train_dir, "images"))
    
    os.makedirs(os.path.join(ROOT_DIR, "val"))
    val_dir = os.path.join(ROOT_DIR, "val")
    os.makedirs(os.path.join(val_dir, "images"))

    # Opening JSON file
    with open(os.path.join(tmp_dir, 'annotations.json')) as json_file:
        data = json.load(json_file)

        # 0.1765 is 15% van 100%
        val_keys = random.sample(list(data), round(len(data) * 0.1765))

        validation = {k: v for k, v in data.items() if k in val_keys}
        train = {k: v for k, v in data.items() if k not in val_keys}

    with open(os.path.join(val_dir, SAVE_FILE), 'w') as output_json_file:
        json.dump(validation, output_json_file)

    with open(os.path.join(train_dir, SAVE_FILE), 'w') as output_json_file:
        json.dump(train, output_json_file)
        
    for key, _ in validation.items():
        shutil.move(os.path.join(tmp_dir, "images", key), os.path.join(val_dir, "images", key))

    for key, _ in train.items():
        shutil.move(os.path.join(tmp_dir, "images", key), os.path.join(train_dir, "images"))

    shutil.rmtree(tmp_dir)

    

        




split_test()
json_test()

json_train_val()

# shutil.rmtree(os.path.join(ROOT_DIR, "val"))
# shutil.rmtree(os.path.join(ROOT_DIR, "train"))

split_train_val()