import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import os
import dataTimestamper as dst

baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"

#time = datetime.utcfromtimestamp(1545133022).strftime('%d-%m-%Y %H:%M:%S')

colnames=['EP','StratFirst','EndFirst', 'StartSecond', 'EndSecond']
timestamps = pd.read_csv(baseFolder + 'timestamps.csv', names=colnames, header=0, delimiter=';')

all_empatica_data = {}
# GO through all the folders taht contain empatica
for directory in [x[0] for x in os.walk(baseFolder)]:
    if directory.find("empatica") != -1:
        df = dst.readFiles(directory + "/")
        all_empatica_data[directory.split("/")[-1]] = df



all_empatica_data

#Dataframe with timestamps
