import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from collections import defaultdict

image = "000000026241.jpg"
# image = "000000000308.jpg"
im = Image.open('/media/sander/Elements/datasets/raw_data/COCO_Hand_raw/COCO-Hand-Big/COCO-Hand-Big_Images/' + image)

annotations = defaultdict(list)

with open('/media/sander/Elements/datasets/raw_data/COCO_Hand_raw/COCO-Hand-Big/COCO-Hand-Big_annotations.txt') as f:
    for line in f:
        data = line.split(",")

        #xmin xmax ymin ymax
        if data[0] in annotations:
            annotations[data[0]].append([data[1], data[2], data[3], data[4]])
        else:
            annotations[data[0]] = [[data[1], data[2], data[3], data[4]]]

# # Create figure and axes
fig, ax = plt.subplots()

# # Display the image
ax.imshow(im)

for hand in annotations[image]:    
    # Create a Rectangle patch
    rect = patches.Rectangle((float(hand[0]), float(hand[2])), float(hand[1]) - float(hand[0]), float(hand[3]) - float(hand[2]), linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

plt.show()