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
python pascalvoc.py --gt ../../data/groundtruth/val --det ../../results/yolov5/ -detcoords rel -imgsize 1280,720 --start 0 --stop 0 --step 1
python pascalvoc.py --gt ../../data/groundtruth/val --det ../../results/ExtremeNet/ --start 250 --stop 10000 --step 250 -np
```

