import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"

colnames= ['time', 'participant', 'stress', 'tension', 'concentration', 'emotions']

before_df = pd.read_csv(baseFolder+ "PSS_BEFORE.csv", delimiter=';', header=0,names=colnames)
before_df = before_df.dropna(0, how='all')

after_no_light_df = pd.read_csv(baseFolder + "PSS_AFTER_NO_LIGHT.csv", delimiter=';',header=0, names=colnames)
after_no_light_df = after_no_light_df.dropna(0, how='all')

after_blue_light_df = pd.read_csv(baseFolder + "PSS_AFTER_LIGHT.csv", delimiter=';',header=0, names=colnames)
after_blue_light_df = after_blue_light_df.dropna(0, how='all')
print("stop")

stress_before =
stress_after_no =
stress_after_blue =

y = [0,1,2,3,4,5,6,7,8]

ax = plt.subplot(111)
ax.bar(x-0.2, y,width=0.2,color='b',align='center')
ax.bar(x, z,width=0.2,color='g',align='center')
ax.bar(x+0.2, k,width=0.2,color='r',align='center')
ax.xaxis_date()

plt.show()
