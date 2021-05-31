import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

im = Image.open('../processed_data/mittel_zisserman/images/VOC2007_606.jpg')

# Create figure and axes
fig, ax = plt.subplots()

# Display the image
ax.imshow(im)

# Create a Rectangle patch
rect = patches.Rectangle((156.71247505948114, 216.3627744801092), 31.123436977811906, 32.326738621480956, linewidth=1, edgecolor='r', facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()