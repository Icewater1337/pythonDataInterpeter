import glob

import pandas as pd
import numpy as np
import os
from fnmatch import fnmatch
import re



''' 
This class reads HR files and extracts the min max for each person with the timestamp.
'''


def return_row_with_min_max(hr_df, filename):
    list = []
    ep = re.search('empatica_ep_(.*).splitParts', filename).group(1)
    min = np.min(hr_df['hr'])
    min_time_index = int(hr_df[hr_df['hr']== min].index[0])
    min_time = hr_df.get_value(min_time_index,'Timestamp')
    max = np.max(hr_df['hr'])
    max_time_index = int(hr_df[hr_df['hr'] == max].index[0])
    max_time = hr_df.get_value(max_time_index,'Timestamp')

    list.append(ep)
    list.append(re.search('splitParts..HR(.*).csv',filename).group(1))
    list.append(min_time)
    list.append(min)
    list.append(max_time)
    list.append(max)

    return list


def read_hr_files_as_df_with_min_max(folder):
    colnames= ['ep', 'type', 'timestamp_low', 'low', 'timestamp_high', 'high']
    final_list = []
    pattern = "*.csv"

    for path, subdirs, files in os.walk(folder):
        if path.find('splitParts') != -1:
            for name in files:
                if fnmatch(name, pattern) and name.find('HR') != -1:
                    filePath = os.path.join(path, name)
                    final_list.append(return_row_with_min_max(pd.read_csv(filePath,header=0), filePath))

    final_df = pd.DataFrame(final_list, columns=colnames)
    return final_df



bf = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"
df_to_save = read_hr_files_as_df_with_min_max(bf)
df_to_save.to_csv(bf+"minmaxHr.csv", index= False)