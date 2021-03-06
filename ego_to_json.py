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

ROOT_DIR = "../egohands_data"
ANNOTATION_FILE = "polygons.mat"
SAVE_FILE = "annotations.json"


def split_test():
    os.makedirs(os.path.join(ROOT_DIR, "test"))
    os.makedirs(os.path.join(ROOT_DIR, "val"))
    os.makedirs(os.path.join(ROOT_DIR, "train"))
    
    shutil.move(os.path.join(ROOT_DIR, "CARDS_COURTYARD_B_T"), os.path.join(ROOT_DIR, "test", "CARDS_COURTYARD_B_T"))
    shutil.move(os.path.join(ROOT_DIR, "CARDS_OFFICE_S_B"), os.path.join(ROOT_DIR, "test", "CARDS_OFFICE_S_B"))
    shutil.move(os.path.join(ROOT_DIR, "CHESS_COURTYARD_B_T"), os.path.join(ROOT_DIR, "test", "CHESS_COURTYARD_B_T"))
    shutil.move(os.path.join(ROOT_DIR, "CHESS_LIVINGROOM_T_H"), os.path.join(ROOT_DIR, "test", "CHESS_LIVINGROOM_T_H"))   
    shutil.move(os.path.join(ROOT_DIR, "JENGA_LIVINGROOM_S_T"), os.path.join(ROOT_DIR, "test", "JENGA_LIVINGROOM_S_T"))
    shutil.move(os.path.join(ROOT_DIR, "JENGA_OFFICE_H_T"), os.path.join(ROOT_DIR, "test", "JENGA_OFFICE_H_T"))
    shutil.move(os.path.join(ROOT_DIR, "PUZZLE_COURTYARD_H_T"), os.path.join(ROOT_DIR, "test", "PUZZLE_COURTYARD_H_T"))
    shutil.move(os.path.join(ROOT_DIR, "PUZZLE_LIVINGROOM_T_B"), os.path.join(ROOT_DIR, "test", "PUZZLE_LIVINGROOM_T_B"))

    shutil.move(os.path.join(ROOT_DIR, "CARDS_LIVINGROOM_S_H"), os.path.join(ROOT_DIR, "val", "CARDS_LIVINGROOM_S_H"))
    shutil.move(os.path.join(ROOT_DIR, "CHESS_COURTYARD_H_S"), os.path.join(ROOT_DIR, "val", "CHESS_COURTYARD_H_S"))
    shutil.move(os.path.join(ROOT_DIR, "JENGA_COURTYARD_T_S"), os.path.join(ROOT_DIR, "val", "JENGA_COURTYARD_T_S"))
    shutil.move(os.path.join(ROOT_DIR, "PUZZLE_OFFICE_S_T"), os.path.join(ROOT_DIR, "val", "PUZZLE_OFFICE_S_T"))

    train = ['CARDS_COURTYARD_H_S','CARDS_COURTYARD_S_H','CARDS_COURTYARD_T_B','CARDS_LIVINGROOM_B_T','CARDS_LIVINGROOM_H_S','CARDS_LIVINGROOM_T_B','CARDS_OFFICE_B_S','CARDS_OFFICE_H_T','CARDS_OFFICE_T_H','CHESS_COURTYARD_S_H','CHESS_COURTYARD_T_B','CHESS_LIVINGROOM_B_S','CHESS_LIVINGROOM_H_T','CHESS_LIVINGROOM_S_B','CHESS_OFFICE_B_S','CHESS_OFFICE_H_T','CHESS_OFFICE_S_B','CHESS_OFFICE_T_H','JENGA_COURTYARD_B_H','JENGA_COURTYARD_H_B','JENGA_COURTYARD_S_T','JENGA_LIVINGROOM_B_H','JENGA_LIVINGROOM_H_B','JENGA_LIVINGROOM_T_S','JENGA_OFFICE_B_S','JENGA_OFFICE_S_B','JENGA_OFFICE_T_H','PUZZLE_COURTYARD_B_S','PUZZLE_COURTYARD_S_B','PUZZLE_COURTYARD_T_H','PUZZLE_LIVINGROOM_B_T','PUZZLE_LIVINGROOM_H_S','PUZZLE_LIVINGROOM_S_H','PUZZLE_OFFICE_B_H','PUZZLE_OFFICE_H_B','PUZZLE_OFFICE_T_S']

    for folder in train:
        shutil.move(os.path.join(ROOT_DIR, folder), os.path.join(ROOT_DIR, "train", folder))

def json_test():
    # test_dir = os.path.join(ROOT_DIR, "test")
    # os.makedirs(os.path.join(test_dir, "images"))
    # img_dir = os.path.join(test_dir, "images")

    # create_annotations(test_dir,img_dir)

    # val_dir = os.path.join(ROOT_DIR, "val")
    # os.makedirs(os.path.join(val_dir, "images"))
    # img_dir = os.path.join(val_dir, "images")

    # create_annotations(val_dir,img_dir)

    train_dir = os.path.join(ROOT_DIR, "train")
    # os.makedirs(os.path.join(train_dir, "images"))
    img_dir = os.path.join(train_dir, "images")

    create_annotations(train_dir,img_dir)

   
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

        # 0.1765 is 15% van 100% omdat test al 20 % is (niet helemaal)
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

def move_to_folder():
    os.makedirs(os.path.join(ROOT_DIR, "json"))
    json_dir = os.path.join(ROOT_DIR, "json")
    shutil.move(os.path.join(ROOT_DIR, "test"), json_dir)
    shutil.move(os.path.join(ROOT_DIR, "val"), json_dir)
    shutil.move(os.path.join(ROOT_DIR, "train"), json_dir)

    shutil.move(ROOT_DIR, "../data")


# split_test()
json_test()
# json_train_val()
# split_train_val()
move_to_folder()