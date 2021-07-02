import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from collections import defaultdict

image = "VOC2007_37.jpg"
# image = "000000000308.jpg"
im = Image.open('/media/sander/Elements/datasets/processed_data/mittel_zisserman/images/' + image)

annotations = []

with open('/media/sander/Elements/experiments/experiment_2/test_results_mittel/trident/0/VOC2007_37.txt') as f:
    for line in f:
        data = line.split(" ")
        print(data)
        #xmin xmax ymin ymax
        if float(data[1]) >= 0.50:
                print("groter")
                annotations.append([data[2], data[3], data[4], data[5], data[1]])
    
# # Create figure and axes
fig, ax = plt.subplots()

# # Display the image
ax.imshow(im)
print(annotations)
for hand in annotations:    
    # Create a Rectangle patch
    rect = patches.Rectangle((float(hand[0]), float(hand[1])), float(hand[2]), float(hand[3]), linewidth=1, edgecolor='b', facecolor='none')
    # Add the patch to the Axes
    ax.add_patch(rect)
    ax.annotate("Conf: " + hand[4][0:4], (float(hand[0]), float(hand[1])), color='w', weight='bold', 
                fontsize=6, ha='center', va='center')

plt.axis('off')
plt.savefig("/home/sander/mittal_trident.png", bbox_inches='tight')