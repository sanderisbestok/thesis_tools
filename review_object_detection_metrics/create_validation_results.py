
"""Evaluate and saves results"""
import os
import csv
import src.evaluators.coco_evaluator as coco_evaluator
import src.evaluators.pascal_voc_evaluator as pascal_voc_evaluator
import src.utils.converter as converter
from src.utils.enumerators import BBFormat, BBType, CoordinatesType, MethodAveragePrecision

DIR_GTS = '/media/sander/Elements/datasets/processed_data/mittel_zisserman/annotations'
TOP_DIR_DETS = '/media/sander/Elements/experiments/experiment_2/test_results_mittel/yolov5'

def evaluate(start, stop, step, save_file="results.txt", img_size=None):
    """Evaluate and save coco results"""

    if img_size:
        bb_format = BBFormat.YOLO
    else:
        bb_format = BBFormat.XYWH

    results = []

    for i in range(start, stop+step, step):
        dir_dets = os.path.join(TOP_DIR_DETS, str(i))

        det_bbs = converter.text2bb(dir_dets, bb_type=BBType.DETECTED,
            bb_format=bb_format, type_coordinates=CoordinatesType.ABSOLUTE, img_size=img_size)
        gt_bbs = converter.text2bb(DIR_GTS, bb_type=BBType.GROUND_TRUTH,
            bb_format=BBFormat.XYWH, type_coordinates=CoordinatesType.ABSOLUTE, img_size=img_size)


        result = {"iteration": i}
        coco_res = coco_evaluator.get_coco_summary(gt_bbs, det_bbs)
        dict_res = pascal_voc_evaluator.get_pascalvoc_metrics(gt_bbs, det_bbs, 0.5, generate_table=True, method=MethodAveragePrecision.EVERY_POINT_INTERPOLATION)

        # Merge dicts
        result |= coco_res
        result |= {'Pascal COCO': dict_res['mAP']}
        results.append(result)

        print(i)


    keys = results[0].keys()
    with open(save_file, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

# start, stop, step, img_size
evaluate(0, 0, 1, save_file = "yolov5_ego_new.txt", img_size=None)
