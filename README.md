# thesis_tools

## Results
The three different algorithms produce results in different formats:

Yolo unrelative maken

Standaard class name xywh

1. 


The results can be converted using Object-Detection-Metrics with the following command:

```
python pascalvoc.py --gt ../../data/groundtruth/val --det ../../results/yolov5/ -detcoords rel -imgsize 1280,720 --start 0 --stop 0 --step 1
python pascalvoc.py --gt ../../data/groundtruth/val --det ../../results/ExtremeNet/ --start 250 --stop 10000 --step 250 -np
```

