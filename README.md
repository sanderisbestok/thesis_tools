# thesis_tools

## Results
The three different algorithms produce results in different formats:

Yolo unrelative maken

Standaard classname conf xywh

1. Yolov5 - classname (1) , conf, xywh (relatief) 
2. Extremenet - classname (1), conf, xywh
3. TridentNet - classname (1), conf, xywh


The results can be converted using Object-Detection-Metrics with the following command:

```
python create_results.py --gt ../../data/groundtruth/val --det ../../../experiments/experiment_1/validation_results/yolov5/ -detcoords rel -imgsize 1280,720 --start 0 --stop 131 --step 1
python create_results.py --gt ../../data/groundtruth/val --det ../../../experiments/experiment_1/validation_results/ExtremeNet/ --start 0 --stop 4550 --step 50 -np
python create_results.py --gt ../../data/groundtruth/val --det ../../../experiments/experiment_1/validation_results/trident/ --start 9 --stop 2549 --step 10 -np
```

For the testing:

```
python create_test_results.py --gt ../../data/groundtruth/test/ --det ../../../experiments/experiment_1/test_results_ego/extremenet/ -network extremenet -testset egohands
python create_test_results.py --gt ../../processed_data/mittel_zisserman/annotations/ --det ../../../experiments/experiment_1/test_results_mittel/trident/ -network tridentnet -testset mittal
```

## Clear the following locations
```
~/networks/detectron2/tridentnet_training_output/*

~/networks/extremenet_sander/coco_extreme_train.pkl
~/networks/extremenet_sander/coco_extreme_val.pkl
~/networks/extremenet_sander/cache/nnet/ExtremeNet/*

~/networks/yolov5/runs/train/*
~/networks/yolov5/runs/detect/*


```
