import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import os
import dataTimestamper as dst
import time as time

baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"

# .strftime('%d-%m-%Y %H:%M:%S')


all_empatica_data = {}
# GO through all the folders taht contain empatica
for directory in [x[0] for x in os.walk(baseFolder)]:
    if directory.find("empatica") != -1:
        df = dst.readFiles(directory + "/")
        all_empatica_data[directory.split("/")[-1]] = df

all_empatica_data

#
timestamps = pd.read_csv(baseFolder + 'timestamps.csv', header=0, delimiter=';')
timestamps = timestamps.drop([9], axis=0)
# Loop through all dicts and split all at the given timestamps
for index, row in timestamps.iterrows():
    episode = "empatica_ep_" + str(row['EP']).zfill(2)
    current_ep = all_empatica_data[episode]
    # get the time from the episode
    current_ep_start = datetime.fromtimestamp(current_ep['HR'].iloc[0,].name)
    start_first_arr = row['StartFirst'].split(":")
    start_first = current_ep_start.replace(second=int(start_first_arr[2]), minute=int(start_first_arr[1]),
                                           hour=int(start_first_arr[0]))
    end_first_arr = row['EndFirst'].split(":")
    end_first = current_ep_start.replace(second=int(end_first_arr[2]), minute=int(end_first_arr[1]),
                                         hour=int(end_first_arr[0]))

    start_second_arr = row['StartSecond'].split(":")
    start_second = current_ep_start.replace(second=int(start_second_arr[2]), minute=int(start_second_arr[1]),
                                            hour=int(start_second_arr[0]))

    end_second_arr = row['EndSecond'].split(":")
    end_second = current_ep_start.replace(second=int(end_second_arr[2]), minute=int(end_second_arr[1]),
                                          hour=int(end_second_arr[0]))

    for key, value in current_ep.items():
        #start_idx_first = 0
        #start_idx_second = 0
        #end_idx_first = 0
        #end_idx_second = 0
        first_part = value.loc[np.logical_and(value.index > time.mktime(start_first.timetuple()),
                                              value.index < time.mktime(end_first.timetuple()))]
        second_part = value.loc[np.logical_and(value.index > time.mktime(start_second.timetuple()),
                                               value.index < time.mktime(end_second.timetuple()))]
        #for ro_w in value.iterrows():
            #            date_time = datetime.(ro_w[0])

         #   print(ro_w)

            # date_time = datetime.utcfromtimestamp(ro_w[0])

            # d = datetime.date(2015, 1, 5)

            # unixtime = time.mktime(d.timetuple())

# Dataframe with timestamps
