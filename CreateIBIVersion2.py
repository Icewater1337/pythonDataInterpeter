import os

import numpy as np
import pandas as pd

from downloadedUtils import empaticaHRV

# This class takes the bvp and hr and calculates the ibi for it
# Also splits it in the parts for first and second eperiment

def getAllEmpaticaDataInFolder( baseFolder):
    all_empatica_data = {}
    # GO through all the folders taht contain empatica
    for directory in [x[0] for x in os.walk(baseFolder)]:
        if directory.find("empatica") != -1 and not directory.endswith("splitParts"):
            dict_current_ep = {}
            dict_current_ep['HR'] = pd.read_csv(directory+"/HR.csv")
            dict_current_ep['BVP'] = pd.read_csv(directory+"/BVP.csv")
            all_empatica_data[directory.split("/")[-1]] = dict_current_ep

    return all_empatica_data

def splitALlFiles( baseFolder, allData):
    timestamps = pd.read_csv(baseFolder + 'timestampsUtc.csv', header=0, delimiter=',')

    # Loop through all dicts and split all at the given timestamps
    for index, row in timestamps.iterrows():
        epi = "empatica_ep_" + str(int(row['ep'])).zfill(2)
        #splitEpisode(epi, allData, row, baseFolder)
        splitAndSaveToCsv(allData[epi]['HR'], allData[epi]['BVP'], row, baseFolder)


def splitAndSaveToCsv( HR_DF, BVP_DF,timestamp, baseFolder):
    column = list(HR_DF)[0]
    temp = HR_DF.drop(0, axis=0)
    HR = temp[column]
    HR = HR.tolist()
    part1 = 'blue' if timestamp['ep'] % 2 == 0 else 'noLight'
    part2 = 'noLight' if timestamp['ep'] % 2 == 0 else 'blue'

    column2 = list(BVP_DF)[0]
    sample_rate = BVP_DF[column2][0]
    temp = BVP_DF.drop(0, axis=0)
    temp['spData'] = 0
    temp.loc[temp[column2] > 0, 'spData'] = temp[column2]
    signal = temp['spData'].tolist()
    episode_str = "empatica_ep_"+ str(int(timestamp['ep'])).zfill(2)
    # split here
    RRI_DF = empaticaHRV.getRRI(signal, column2, sample_rate)

    first_part = RRI_DF.loc[np.logical_and(RRI_DF['Timestamp'] > timestamp['start_first'],
                                           RRI_DF['Timestamp'] <timestamp['end_first'] )]

    second_part = RRI_DF.loc[np.logical_and(RRI_DF['Timestamp'] > timestamp['start_second'],
                                            RRI_DF['Timestamp'] <timestamp['end_second'] )]

    first_part.to_csv(baseFolder + episode_str + "/splitParts/1IBI" + part1 + ".csv", index=False)
    second_part.to_csv(baseFolder + episode_str + "/splitParts/2IBI"+ part2 + ".csv", index=False)


