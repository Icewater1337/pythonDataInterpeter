import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import RMSSDHRVCalc as hrvCalc
from os import listdir
from os.path import isfile, join
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

plotly.tools.set_credentials_file(username='Icewater1337', api_key='W7l3xKeSGXQ5oU5XTipP')


def calculateHRVforFirstAndSecondIbi(folder):
    global hrv1, hrv2
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    colnames=['Time','IBI']
    for i in onlyfiles:
        if "IBIblue" in i:
            ibiBlue = pd.read_csv(folder +i, names=colnames, header=0)
            hrv2 = hrvCalc.calculateRMSSDFromIbi(ibiBlue)

        if "IBInoLight" in i:
            ibiNoLight = pd.read_csv(folder + i, names=colnames, header=0)
            hrv1 = hrvCalc.calculateRMSSDFromIbi(ibiNoLight)

    return hrv1,hrv2



epNbrs = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18]
hrv_no_light = []
hrv_with_light = []
# Calculate one ibi

for epNbr in epNbrs:
    baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/empatica_ep_" + str(epNbr).zfill(2) + "/splitParts/"
    hrv1, hrv2 = calculateHRVforFirstAndSecondIbi(baseFolder)
    hrv_no_light.append(hrv1)
    hrv_with_light.append(hrv2)

#epNbr = "04"


twosample_results = ttest_ind( hrv_with_light, hrv_no_light)

matrix_twosample = [
    ['', 'Test Statistic', 'p-value'],
    ['Sample Data', twosample_results[0], twosample_results[1]]
]

twosample_table = FF.create_table(matrix_twosample, index=True)
py.iplot(twosample_table, filename='twosample-table')