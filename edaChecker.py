
import os
import re
from fnmatch import fnmatch

import pandas as pd

def read_hr_files_as_df_with_min_max(folder):

    final_dict = {}
    pattern = "*.csv"

    for path, subdirs, files in os.walk(folder):
        if path.find('splitParts') != -1:
            for name in files:
                if fnmatch(name, pattern) and name.find('EDA') != -1:
                    filePath = os.path.join(path, name)
                    ep = re.search('empatica_ep_(.*).splitParts', path).group(1)
                    final_dict[ep+"_"+name] = (pd.read_csv(filePath))

    return final_dict

bf = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"


list_of_zero_episodes = []
for key, value in read_hr_files_as_df_with_min_max(bf).items():
    result = any(elem < 0.05 for elem in value['eda'])
    if result:
        list_of_zero_episodes.append(key)


print (list_of_zero_episodes)