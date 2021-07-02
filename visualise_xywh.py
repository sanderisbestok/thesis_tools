import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

im = Image.open('../data/extremenet/images/test/CARDS_OFFICE_B_S_frame_0014.jpg')

# Create figure and axes
fig, ax = plt.subplots()

# Display the image
ax.imshow(im)

# Create a Rectangle patch
rect = patches.Rectangle((590, 226), 88, 98, linewidth=1, edgecolor='r', facecolor='none')

# Add the patch to the Axes
ax.add_patch(rect)

plt.show()