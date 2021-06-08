import pandas as pd

import matplotlib.pyplot as plt

data = pd.read_csv('../../experiments/experiment_1/validation_results/yolov5.txt',sep=',',header=None)
data = pd.DataFrame(data)

x = data[0]
y = data[1]

fig = plt.figure()
fig.suptitle('Average Precision of YOLOv5 on the EgoHands validation set', fontsize=13)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Average Precision', fontsize=12)
plt.plot(x, y,'r')
plt.grid()
plt.show()

data = pd.read_csv('../../experiments/experiment_1/validation_results/extremenet.txt',sep=',',header=None)
data = pd.DataFrame(data)

x = data[0]
y = data[1]

fig = plt.figure()
fig.suptitle('Average Precision of ExtremeNet on the EgoHands validation set', fontsize=13)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Average Precision', fontsize=12)
plt.plot(x, y,'g')
plt.grid()
plt.show()

data = pd.read_csv('../../experiments/experiment_1/validation_results/trident.txt',sep=',',header=None)
data = pd.DataFrame(data)

x = data[0]
y = data[1]

fig = plt.figure()
fig.suptitle('Average Precision of TridentNet on the EgoHands validation set', fontsize=13)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Average Precision', fontsize=12)
plt.plot(x, y,'b')
plt.grid()
plt.show()