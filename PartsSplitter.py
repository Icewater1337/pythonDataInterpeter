import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import os
import dataTimestamper as dst
import time as time
import os
import CreateIBIVersion2


# This class is responsible for taking all the empatica files in a given folder and sub folder, and
# split them into the parts of the first and second experiment
# For this to work it also needs a file called "timestampcs.csv" in the given basefolder
# which contains for each participant the start and endtime of the first and second experiment.
# The epatica data needs to be given in the following folder structure:
#   GivenBaseFolder/empatica_ep_0X . Example: /empatica_ep_01  or /empatica_ep_10 needs to be contained in the basefolder.

class PartsSplitter:
    def __init__(self, baseFolder):
        # After this you can chose what plots to create in the main method.
        columns = ['ep', 'start_first', 'end_first', 'start_second', 'end_second']
        self.df_timestamps = pd.DataFrame(columns=columns)
        self.bf = baseFolder

    def splitEpisode(self, episode, all_empatica_data, row, baseFolder):
        current_ep = all_empatica_data[episode]
        # get the time from the episode
        current_ep_start = datetime.fromtimestamp(current_ep['HR'].iloc[0,].name)

        start_first_arr = [int(n) for n in row['StartFirst'].split(":")]
        start_second_arr = [int(n) for n in row['StartSecond'].split(":")]
        end_second_arr = [int(n) for n in row['EndSecond'].split(":")]
        end_first_arr = [int(n) for n in row['EndFirst'].split(":")]

        if 5 < row['EP'] < 13:
            start_first_arr[0] = start_first_arr[0] - 1
            end_first_arr[0] = end_first_arr[0] - 1
            start_second_arr[0] = start_second_arr[0] - 1
            end_second_arr[0] = end_second_arr[0] - 1

        start_first = current_ep_start.replace(second=int(start_first_arr[2]), minute=int(start_first_arr[1]),
                                               hour=int(start_first_arr[0]))
        end_first = current_ep_start.replace(second=int(end_first_arr[2]), minute=int(end_first_arr[1]),
                                             hour=int(end_first_arr[0]))

        start_second = current_ep_start.replace(second=int(start_second_arr[2]), minute=int(start_second_arr[1]),
                                                hour=int(start_second_arr[0]))

        end_second = current_ep_start.replace(second=int(end_second_arr[2]), minute=int(end_second_arr[1]),
                                              hour=int(end_second_arr[0]))

        self.df_timestamps.loc[row['EP']] = [row['EP'], time.mktime(start_first.timetuple()),
                                             time.mktime(end_first.timetuple()),
                                             time.mktime(start_second.timetuple()), time.mktime(end_second.timetuple())]

        for key, value in current_ep.items():
            part1 = 'blue' if row['EP'] % 2 == 0 else 'noLight'
            part2 = 'noLight' if row['EP'] % 2 == 0 else 'blue'
            # Split in experiment parts
            first_part = value.loc[np.logical_and(value.index > time.mktime(start_first.timetuple()),
                                                  value.index < time.mktime(end_first.timetuple()))]
            first_part.index.name = "Timestamp"
            second_part = value.loc[np.logical_and(value.index > time.mktime(start_second.timetuple()),
                                                   value.index < time.mktime(end_second.timetuple()))]
            second_part.index.name = "Timestamp"

            # create folder
            if not os.path.exists(baseFolder + episode + "/splitParts/"):
                os.makedirs(baseFolder + episode + "/splitParts/")

        # Save to csv.
            if key != "IBI":
                first_part.to_csv(baseFolder + episode + "/splitParts/1" + key + part1 + ".csv", index=True)
                second_part.to_csv(baseFolder + episode + "/splitParts/2" + key + part2 + ".csv", index=True)

    # .strftime('%d-%m-%Y %H:%M:%S')

    def getAllEmpaticaDataInFolder(self, baseFolder):
        all_empatica_data = {}
        # GO through all the folders taht contain empatica
        for directory in [x[0] for x in os.walk(baseFolder)]:
            if directory.find("empatica") != -1 and not directory.endswith("splitParts"):
                df = dst.readFiles(directory + "/")
                all_empatica_data[directory.split("/")[-1]] = df

        return all_empatica_data

    #
    def splitALlFiles(self):
        allData = self.getAllEmpaticaDataInFolder(self.bf)
        timestamps = pd.read_csv(self.bf + 'timestamps.csv', header=0, delimiter=';')
        timestamps = timestamps.drop([9], axis=0)
        # Loop through all dicts and split all at the given timestamps
        for index, row in timestamps.iterrows():
            epi = "empatica_ep_" + str(row['EP']).zfill(2)
            self.splitEpisode(epi, allData, row, self.bf)

        self.df_timestamps.to_csv(self.bf + 'timestampsUtc.csv', index=False)
        self.createIBIManually()

    def createIBIManually(self):
        all_data = CreateIBIVersion2.getAllEmpaticaDataInFolder(self.bf)
        CreateIBIVersion2.splitALlFiles(self.bf, all_data)
