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

import empaticaHRV

plotly.tools.set_credentials_file(username='Icewater1337', api_key='W7l3xKeSGXQ5oU5XTipP')

epNbrs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18]


def calculateHRVforFirstAndSecondIbi(folder):
    global hrv1, hrv2

    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    colnames = ['Time', 'IBI']
    for i in onlyfiles:
        if "IBIblue" in i:
            ibiBlue = pd.read_csv(folder + i, names=colnames, header=0)
            hrv2 = hrvCalc.calculateRMSSDFromIbi(ibiBlue)

        if "IBInoLight" in i:
            ibiNoLight = pd.read_csv(folder + i, names=colnames, header=0)
            hrv1 = hrvCalc.calculateRMSSDFromIbi(ibiNoLight)

    return hrv1, hrv2

def calculateHRVforFirstAndSecondIbiWithAlternativeIbi(folder):
    global hrv1, hrv2

    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    colnames = ['IBI', 'Timestamp']
    for i in onlyfiles:
        if "OwnMade2IBIblue" in i:
            ibiBlue = pd.read_csv(folder + i, names=colnames, header=0)
            hrv2 = hrvCalc.calculateRMSSDFromIbi(ibiBlue)
            #b, c = hrv2.iloc[0].copy(), hrv2.iloc[1].copy()
            #hrv2.iloc[0], hrv2.iloc[1] = c, b

        if "OwnMade1IBInoLight" in i:
            ibiNoLight = pd.read_csv(folder + i, names=colnames, header=0)
            hrv1 = hrvCalc.calculateRMSSDFromIbi(ibiNoLight)
            #b, c = hrv1.iloc[0].copy(), hrv1.iloc[1].copy()
            #hrv1.iloc[0], hrv1.iloc[1] = c, b

    return hrv1, hrv2


def getIBIFromHRAndBVP(HR_DF, BVP_DF):
    column = list(HR_DF)[0]
    temp = HR_DF.drop(0, axis=0)
    HR = temp[column]
    HR = HR.tolist()

    column2 = list(BVP_DF)[0]
    sample_rate = BVP_DF[column2][0]
    temp = BVP_DF.drop(0, axis=0)
    temp['spData'] = 0
    temp.loc[temp[column2] > 0, 'spData'] = temp[column2]
    signal = temp['spData'].tolist()

    return empaticaHRV.getRRI(signal, column2, sample_rate)

def calculateHRVWithFirstTest(folder):
    global hrv1
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    colnames = ['Time', 'IBI']
    for i in onlyfiles:
        if "1IBI" in i:
            ibi = pd.read_csv(folder + i, names=colnames, header=0)
            hrv1 = hrvCalc.calculateRMSSDFromIbi(ibi)
    return hrv1


def getEDA(folder):
    global eda1, eda2
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    colnames = ['Time', 'EDA']
    for i in onlyfiles:
        if "EDAblue" in i:
            eda2 = pd.read_csv(folder + i, names=colnames, header=0)

        if "EDAnoLight" in i:
            eda1 = pd.read_csv(folder + i, names=colnames, header=0)
    return eda1, eda2


def getHR(folder):
    global hr1, hr2
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    colnames = ['Time', 'HR']
    for i in onlyfiles:
        if "HRblue" in i:
            hr2 = pd.read_csv(folder + i, names=colnames, header=0)

        if "HRnoLight" in i:
            hr1 = pd.read_csv(folder + i, names=colnames, header=0)
    return hr1, hr2


def getHRAvgAndTTest():
    hr_no_light = []
    hr_with_light = []
    even = 0
    uneven = 0

    for epNbr in epNbrs:
        baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/empatica_ep_" + str(epNbr).zfill(
            2) + "/splitParts/"
        hr1, hr2 = getHR(baseFolder)
        hr1Avg = np.average(hr1['HR'])
        hr2Avg = np.average(hr2['HR'])



        if ( hr1Avg > 0 and hr2Avg > 0 ):
            if epNbr != 11 and epNbr != 13 and epNbr != 4:
                if epNbr % 2 == 0:
                    even = even + 1
                if epNbr % 2 != 0:
                    uneven = uneven + 1
               # print("Add EP: " + str(epNbr))
               # print("Avg No Light: " + str(hr1Avg))
               # print("Avg With Light: " + str(hr2Avg))
                hr_no_light.append(hr1Avg)
                hr_with_light.append(hr2Avg)

    print("Uneven:" + str(uneven))
    print("even:" + str(even))

    print("Average With light:" + str(np.average(hr_with_light)))
    print("Average Without light:" + str(np.average(hr_no_light)))

    return ttest_ind(hr_no_light, hr_with_light)


def getEDAAvgsAndTTest():
    eda_no_light = []
    eda_with_light = []
    even = 0
    uneven = 0

    for epNbr in epNbrs:
        baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/empatica_ep_" + str(epNbr).zfill(
            2) + "/splitParts/"
        eda1, eda2 = getEDA(baseFolder)
        eda1Avg = np.average(eda1['EDA'])
        eda2Avg = np.average(eda2['EDA'])



        if ( eda1Avg > 0 and eda2Avg > 0 ):
            if epNbr != 11:# and epNbr != 13 and epNbr != 4:
                if epNbr % 2 == 0:
                    even = even + 1
                if epNbr % 2 != 0:
                    uneven = uneven + 1
                #print("Add EP: " + str(epNbr))
                normalizedEda1 = (eda1['EDA']- np.min(eda1['EDA'])) / (np.max(eda1['EDA'])-np.min(eda1['EDA']))
                normalizedEda2 = (eda2['EDA']- np.min(eda2['EDA'])) / (np.max(eda2['EDA'])-np.min(eda2['EDA']))
                #print("Avg No Light: " + str(np.average(normalizedEda1)))
                #print("Avg With Light: " + str(np.average(normalizedEda2)))
                eda_no_light.append(np.average((normalizedEda1)))
                eda_with_light.append(np.average((normalizedEda2)))

    print("Uneven:" + str(uneven))
    print("even:" + str(even))

    print("Average With light:" + str(np.average(eda_with_light)))
    print("Average Without light:" + str(np.average(eda_no_light)))

    return ttest_ind(eda_with_light, eda_no_light)


def getHRVAvgsAndTTest():
    hrv_no_light = []
    hrv_with_light = []
    # Calculate one ibi
    even = 0
    uneven = 0
    for epNbr in epNbrs:

        baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/empatica_ep_" + str(epNbr).zfill(
            2) + "/splitParts/"
        #hrv1, hrv2 = calculateHRVforFirstAndSecondIbi(baseFolder)
        hrv1, hrv2 = calculateHRVforFirstAndSecondIbiWithAlternativeIbi(baseFolder)

        # Read EDA

        if hrv1 > 0 and hrv2 > 0:
            if epNbr != 11:#and epNbr != 13 and epNbr != 4
               # print("add: " + str(epNbr))
               # print(hrv1)
               # print(hrv2)
                if epNbr % 2 == 0:
                    even = even + 1
                if epNbr % 2 != 0:
                    uneven = uneven + 1
                hrv_no_light.append(hrv1)
                hrv_with_light.append(hrv2)

    # epNbr = "04"

    print("Uneven:" + str(uneven))
    print("even:" + str(even))

    print("Average With light:" + str(np.average(hrv_with_light)))
    print("Average Without light:" + str(np.average(hrv_no_light)))

    return ttest_ind(hrv_no_light, hrv_with_light)


def useOnlyPartOneFromTestGetHRV():
    hrv_no_light = []
    hrv_with_light = []
    # Calculate one ibi
    even = 0
    uneven = 0
    for epNbr in epNbrs:

        baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/empatica_ep_" + str(epNbr).zfill(
            2) + "/splitParts/"
        hrv = calculateHRVWithFirstTest(baseFolder)

        # Read EDA

        if hrv > 0:
            #if epNbr != 11 and epNbr != 13:
            print("add: " + str(epNbr))
            print(hrv)
            if epNbr % 2 == 0:
                even = even + 1
                hrv_with_light.append(hrv)
            if epNbr % 2 != 0:
                uneven = uneven + 1
                hrv_no_light.append(hrv)


    # epNbr = "04"

    print("Uneven:" + str(uneven))
    print("even:" + str(even))

    print("Average With light:" + str(np.average(hrv_with_light)))
    print("Average Without light:" + str(np.average(hrv_no_light)))

    return ttest_ind(hrv_no_light, hrv_with_light)



#print(useOnlyPartOneFromTestGetHRV())
print(getEDAAvgsAndTTest())
print(getHRVAvgsAndTTest())
print(getHRAvgAndTTest())
print("Done")
