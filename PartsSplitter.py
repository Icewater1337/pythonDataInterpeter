import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import os
import dataTimestamper as dst
import time as time
import os


def splitEpisode(episode, all_empatica_data, row, baseFolder):
    current_ep = all_empatica_data[episode]
    # get the time from the episode
    current_ep_start = datetime.fromtimestamp(current_ep['HR'].iloc[0,].name)

    start_first_arr = [int(n) for n in row['StartFirst'].split(":")]
    start_second_arr = [int(n) for n in row['StartSecond'].split(":")]
    end_second_arr = [int(n) for n in row['EndSecond'].split(":")]
    end_first_arr = [int(n) for n in row['EndFirst'].split(":")]

    if 5 < row['EP'] < 13:
        start_first_arr[0] = start_first_arr[0]-1
        end_first_arr[0] = end_first_arr[0]-1
        start_second_arr[0] = start_second_arr[0]-1
        end_second_arr[0] = end_second_arr[0]-1

    start_first = current_ep_start.replace(second=int(start_first_arr[2]), minute=int(start_first_arr[1]),
                                           hour=int(start_first_arr[0]))
    end_first = current_ep_start.replace(second=int(end_first_arr[2]), minute=int(end_first_arr[1]),
                                         hour=int(end_first_arr[0]))

    start_second = current_ep_start.replace(second=int(start_second_arr[2]), minute=int(start_second_arr[1]),
                                            hour=int(start_second_arr[0]))

    end_second = current_ep_start.replace(second=int(end_second_arr[2]), minute=int(end_second_arr[1]),
                                          hour=int(end_second_arr[0]))

    for key, value in current_ep.items():
        part1 = 'blue' if row['EP'] % 2 == 0 else 'noLight'
        part2 = 'noLight' if row['EP'] % 2 == 0 else 'blue'
        #Split in experiment parts
        first_part = value.loc[np.logical_and(value.index > time.mktime(start_first.timetuple()),
                                              value.index < time.mktime(end_first.timetuple()))]
        first_part.index.name="Timestamp"
        second_part = value.loc[np.logical_and(value.index > time.mktime(start_second.timetuple()),
                                               value.index < time.mktime(end_second.timetuple()))]
        second_part.index.name = "Timestamp"

        # create folder
        if not os.path.exists(baseFolder+episode+"/splitParts/"):
            os.makedirs(baseFolder+episode+"/splitParts/")
        # Save to csv.
        first_part.to_csv(baseFolder+episode+"/splitParts/1" +key + part1+".csv", index=True)
        second_part.to_csv(baseFolder+episode+"/splitParts/2" +key + part2+".csv", index=True)


# .strftime('%d-%m-%Y %H:%M:%S')

def getAllEmpaticaDataInFolder(baseFolder):
    all_empatica_data = {}
    # GO through all the folders taht contain empatica
    for directory in [x[0] for x in os.walk(baseFolder)]:
        if directory.find("empatica") != -1 and not directory.endswith("splitParts"):
            df = dst.readFiles(directory + "/")
            all_empatica_data[directory.split("/")[-1]] = df

    return all_empatica_data


#
def splitALlFiles(baseFolder, allData):
    timestamps = pd.read_csv(baseFolder + 'timestamps.csv', header=0, delimiter=';')
    timestamps = timestamps.drop([9], axis=0)
    # Loop through all dicts and split all at the given timestamps
    for index, row in timestamps.iterrows():
        epi = "empatica_ep_" + str(row['EP']).zfill(2)
        splitEpisode(epi, allData, row, baseFolder)


bf = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"
splitALlFiles(bf, getAllEmpaticaDataInFolder(bf))