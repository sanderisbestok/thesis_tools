import pandas as pd
data = pd.read_csv('../results/yolov5.txt',sep=',',header=None)
data = pd.DataFrame(data)

import matplotlib.pyplot as plt
x = data[0]
y = data[1]

fig = plt.figure()
fig.suptitle('YoloV5 Average Precision', fontsize=14)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Average Precision', fontsize=12)
plt.plot(x, y,'r')
plt.show()