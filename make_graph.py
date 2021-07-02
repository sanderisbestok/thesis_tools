import pandas as pd

import matplotlib.pyplot as plt

data = pd.read_csv('../../experiments/experiment_2/validation_results/yolov5.txt',sep=',',header=None)
data = pd.DataFrame(data)

new_header = data.iloc[0] #grab the first row for the header
data = data[1:] #take the data less the header row
data.columns = new_header #set the header row as the data header

data = data.astype({'iteration': int, 'AP': float})

first_row = [] 
first_row.insert(0, {'iteration': 0, 'AP': 0, 'AP50': 0, 'AP75': 0, 'APsmall': 0, 'APmedium': 0, 'APlarge': 0, 'AR1': 0, 'AR10': 0, 'AR100': 0, 'ARsmall': 0, 'ARmedium': 0, 'ARlarge': 0})

# batch size of 16 makes 211 iterations per epoch
data["iteration"] = (data["iteration"] * 899) + 899
data = pd.concat([pd.DataFrame(first_row), data], ignore_index=True)

x = data["iteration"]
y = data["AP"]

fig = plt.figure()
fig.suptitle('COCO Average Precision of YOLOv5 on \n the COCO Hands Segmented validation set', fontsize=13)
plt.xlabel('Iteration', fontsize=12)
plt.ylabel('COCO Average Precision', fontsize=12)
plt.plot(x, y,'r')
plt.ylim([0, 1])
plt.grid()
plt.show()

data = pd.read_csv('../../experiments/experiment_2/validation_results/extremenet.txt',sep=',',header=None)
data = pd.DataFrame(data)

new_header = data.iloc[0] #grab the first row for the header
data = data[1:] #take the data less the header row
data.columns = new_header #set the header row as the data header

data = data.astype({'iteration': int, 'AP': float})

x = data["iteration"]
y = data["AP"]

fig = plt.figure()
fig.suptitle('COCO Average Precision of ExtremeNet on \n the COCO Hands Segmented validation set', fontsize=13)
plt.xlabel('Iteration', fontsize=12)
plt.ylabel('COCO Average Precision', fontsize=12)
plt.plot(x, y,'g')
plt.ylim([0, 1])
plt.grid()
plt.show()

data = pd.read_csv('../../experiments/experiment_2/validation_results/trident.txt',sep=',',header=None)
data = pd.DataFrame(data)

new_header = data.iloc[0] #grab the first row for the header
data = data[1:] #take the data less the header row
data.columns = new_header #set the header row as the data header

data = data.astype({'iteration': int, 'AP': float})

x = data["iteration"]
y = data["AP"]

fig = plt.figure()
fig.suptitle('COCO Average Precision of TridentNet on \n the COCO Hands Segmented validation set', fontsize=13)
plt.xlabel('Iteration', fontsize=12)
plt.ylabel('COCO Average Precision', fontsize=12)
plt.plot(x, y,'b')
plt.ylim([0, 1])
plt.grid()
plt.show()