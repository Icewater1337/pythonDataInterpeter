import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"

time = datetime.utcfromtimestamp(1545133022).strftime('%d-%m-%Y %H:%M:%S')

colnames=['EP','StratFirst','EndFirst', 'StartSecond', 'EndSecond']
timestamps = pd.read_csv(baseFolder + 'timestamps.csv', names=colnames, header=0, delimiter=';')

timestamps



#Dataframe with timestamps
