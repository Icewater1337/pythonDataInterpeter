from os import listdir
from os.path import isfile, join

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, stats

import HRVCalcs as hrvCalc
from downloadedUtils import empaticaHRV


# This class contains the methods to do the physiological analysis.
# Its constructor takes two arguments:
# 1. The folder where the data lies. For now this folder has to contain folders that follow this naming convention:
#   baseFolder/empatica_ep_X/splitParts Whereas splitParts subfolder contains the data for only first experiment
# And the data for the second experiment.
# The naming conventions for the single files are the following: Part + Type + light setting
# Example: 1BVPnoLight or 2IBIblue  Where the part is whether it was MAT one or MAT two
# 2. epNbrs which contains the episodes to look at. Episodes not in there will be ignored.
def printAvgMeanStdVar(with_light, without_light):
    print("Average With light:" + str(np.average(with_light)))
    print("Average Without light:" + str(np.average(without_light)))
    print("Mean With light:" + str(np.mean(with_light)))
    print("Mean Without light:" + str(np.mean(without_light)))
    print("Standard deviation With light:" + str(np.std(with_light)))
    print("Standard deviation Without light:" + str(np.std(without_light)))
    print("Variance With light:" + str(np.var(with_light)))
    print("Variance Without light:" + str(np.var(without_light)))

class PhysiologicalAnalysis:
    def __init__(self, baseFolder, epNbrs):
        # After this you can chose what plots to create in the main method.
        self.baseFolder = baseFolder
        self.epNbrs = epNbrs

    def calculateHRVRMSSDforFirstAndSecondIbi(self, folder):
        global hrv1, hrv2

        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        colnames = ['IBI', 'Time']
        for i in onlyfiles:
            if "IBIblue" in i:
                ibiBlue = pd.read_csv(folder + i, names=colnames, header=0)
                hrv2 = hrvCalc.calculateRMSSDFromIbi(ibiBlue)

            if "IBInoLight" in i:
                ibiNoLight = pd.read_csv(folder + i, names=colnames, header=0)
                hrv1 = hrvCalc.calculateRMSSDFromIbi(ibiNoLight)

        return hrv1, hrv2

    def calculateHRVRMSSDforBaseIbi(self, folder):
        global  hrv2

        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        colnames = ['IBI', 'Time']
        for i in onlyfiles:
            if "IBIBase" in i:
                ibiBlue = pd.read_csv(folder + i, names=colnames, header=0)
                hrv2 = hrvCalc.calculateRMSSDFromIbi(ibiBlue)

        return hrv2

    def calculateHRVSDRRforFirstAndSecondIbi(self, folder):
        global hrv1, hrv2

        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        colnames = ['IBI', 'Time']
        for i in onlyfiles:
            if "IBIblue" in i:
                ibiBlue = pd.read_csv(folder + i, names=colnames, header=0)
                hrv2 = hrvCalc.calculateSDRRFromIbi(ibiBlue)

            if "IBInoLight" in i:
                ibiNoLight = pd.read_csv(folder + i, names=colnames, header=0)
                hrv1 = hrvCalc.calculateSDRRFromIbi(ibiNoLight)

        return hrv1, hrv2

    def getIBIFromHRAndBVP(self, HR_DF, BVP_DF):
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

    def calculateHRVWithFirstTest(self, folder):
        global hrv1
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        colnames = ['IBI', 'Time']
        for i in onlyfiles:
            if "1IBI" in i:
                ibi = pd.read_csv(folder + i, names=colnames, header=0)
                hrv1 = hrvCalc.calculateRMSSDFromIbi(ibi)
        return hrv1

    def getEDA(self, folder):
        global eda1, eda2
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        colnames = ['Time', 'EDA']
        for i in onlyfiles:
            if "EDAblue" in i:
                eda2 = pd.read_csv(folder + i, names=colnames, header=0)

            if "EDAnoLight" in i:
                eda1 = pd.read_csv(folder + i, names=colnames, header=0)
        return eda1, eda2

    def getHR(self, folder):
        global hr1, hr2
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        colnames = ['Time', 'HR']
        for i in onlyfiles:
            if "HRblue" in i:
                hr2 = pd.read_csv(folder + i, names=colnames, header=0)

            if "HRnoLight" in i:
                hr1 = pd.read_csv(folder + i, names=colnames, header=0)
        return hr1, hr2

    def getBaseHR(self, folder):
        global hr2
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        colnames = ['Time', 'HR']
        for i in onlyfiles:
            if "HRbasePart" in i:
                hr2 = pd.read_csv(folder + i, names=colnames, header=0)
        return hr2

    # This method takes all HR data and creates a T-test with it
    def getHRAvgAndTTest(self):
        hr_no_light = []
        hr_with_light = []
        even = 0
        uneven = 0

        for epNbr in self.epNbrs:
            baseFolder = self.baseFolder + "empatica_ep_" + str(epNbr).zfill(
                2) + "/splitParts/"
            hr1, hr2 = self.getHR(baseFolder)
            hr1Avg = np.average(hr1['HR'])
            hr2Avg = np.average(hr2['HR'])

            if (hr1Avg > 0 and hr2Avg > 0):
                if epNbr % 2 == 0:
                    even = even + 1
                if epNbr % 2 != 0:
                    uneven = uneven + 1
                    # print("Add EP: " + str(epNbr))
                    # print("Avg No Light: " + str(hr1Avg))
                    # print("Avg With Light: " + str(hr2Avg))
                hr_no_light.append(hr1Avg)
                hr_with_light.append(hr2Avg)



        return hr_no_light, hr_with_light, even, uneven

    # This method takes the EDA and calculates a t-test on it
    def getEDAAndAvgs(self):
        eda_no_light = []
        eda_with_light = []
        even = 0
        uneven = 0

        for epNbr in self.epNbrs:
            baseFolder = self.baseFolder + "empatica_ep_" + str(epNbr).zfill(
                2) + "/splitParts/"
            eda1, eda2 = self.getEDA(baseFolder)
            eda1Avg = np.average(eda1['EDA'])
            eda2Avg = np.average(eda2['EDA'])

            if (eda1Avg > 0 and eda2Avg > 0):
                if epNbr % 2 == 0:
                    even = even + 1
                if epNbr % 2 != 0:
                    uneven = uneven + 1
                # print("Add EP: " + str(epNbr))
                normalizedEda1 = (eda1['EDA'] - np.min(eda1['EDA'])) / (np.max(eda1['EDA']) - np.min(eda1['EDA']))
                normalizedEda2 = (eda2['EDA'] - np.min(eda2['EDA'])) / (np.max(eda2['EDA']) - np.min(eda2['EDA']))
                # print("Avg No Light: " + str(np.average(normalizedEda1)))
                # print("Avg With Light: " + str(np.average(normalizedEda2)))
                eda_no_light.append(np.average((normalizedEda1)))
                eda_with_light.append(np.average((normalizedEda2)))


        return eda_no_light, eda_with_light, even, uneven

    def getEDAValuesAndTTest(self):
        eda_no_light, eda_with_light, even, uneven = self.getEDAAndAvgs()
        print("No Light Start:" + str(uneven))
        print("Blue light start:" + str(even))

        printAvgMeanStdVar(eda_with_light, eda_no_light)

        print(self.calculateTTest(eda_with_light, eda_no_light))

    def getHRVRMSSDAvgsAndTTest(self):
        hrv_no_light = []
        hrv_with_light = []
        # Calculate one ibi
        even = 0
        uneven = 0
        for epNbr in self.epNbrs:

            baseFolder = self.baseFolder + "empatica_ep_" + str(epNbr).zfill(
                2) + "/splitParts/"
            # hrv1, hrv2 = calculateHRVforFirstAndSecondIbi(baseFolder)
            hrv1, hrv2 = self.calculateHRVRMSSDforFirstAndSecondIbi(baseFolder)

            # Read EDA

            if hrv1 > 0 and hrv2 > 0:
                # print("add: " + str(epNbr))
                # print(hrv1)
                # print(hrv2)
                if epNbr % 2 == 0:
                    even = even + 1
                if epNbr % 2 != 0:
                    uneven = uneven + 1
                hrv_no_light.append(hrv1)
                hrv_with_light.append(hrv2)

        #print("No Light Start:" + str(uneven))
        #print("Blue light start:" + str(even))

        #printAvgMeanStdVar(hrv_with_light, hrv_no_light)

    #    print(self.calculateTTest(hrv_with_light, hrv_no_light))

        return hrv_no_light, hrv_with_light, even, uneven

    def getHRVSDRRAvgsAndTTest(self):
        hrv_no_light = []
        hrv_with_light = []
        # Calculate one ibi
        even = 0
        uneven = 0
        for epNbr in self.epNbrs:

            baseFolder = self.baseFolder + "empatica_ep_" + str(epNbr).zfill(
                2) + "/splitParts/"
            # hrv1, hrv2 = calculateHRVforFirstAndSecondIbi(baseFolder)
            hrv1, hrv2 = self.calculateHRVSDRRforFirstAndSecondIbi(baseFolder)

            # Read EDA

            if hrv1 > 0 and hrv2 > 0:
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
        # print(hrv_no_light)
        # print(hrv_with_light)

        return hrv_no_light, hrv_with_light,even, uneven

    def getHrvRMSSD(self):
        hrv_no_light, hrv_with_light,even, uneven = self.getHRVRMSSDAvgsAndTTest()
        print("No Light Start:" + str(uneven))
        print("Blue light start:" + str(even))

        printAvgMeanStdVar(hrv_with_light, hrv_no_light)

        print(self.calculateTTest(hrv_with_light, hrv_no_light))

    def getHRVSDRR(self):
        hrv_no_light, hrv_with_light, even, uneven = self.getHRVSDRRAvgsAndTTest()
        print("No Light Start:" + str(uneven))
        print("Blue light start:" + str(even))

        printAvgMeanStdVar(hrv_with_light, hrv_no_light)

        print(self.calculateTTest(hrv_with_light, hrv_no_light))

    def getHr(self):
        hr_no_light, hr_with_light, even, uneven = self.getHRAvgAndTTest()
        print("No Light Start:" + str(uneven))
        print("Blue light start:" + str(even))

        printAvgMeanStdVar(hr_with_light, hr_no_light)

        print(self.calculateTTest(hr_with_light, hr_no_light))


    def calculateTTest(self, with_light, no_light):
        return ttest_ind(with_light, no_light, equal_var=True)



    # This method only takes the first part of the experiment. The first MAT task.
    def useOnlyPartOneFromTestGetHRV(self):
        hrv_no_light = []
        hrv_with_light = []
        # Calculate one ibi
        even = 0
        uneven = 0
        for epNbr in self.epNbrs:

            baseFolder = self.baseFolder + "empatica_ep_" + str(epNbr).zfill(
                2) + "/splitParts/"
            hrv = self.calculateHRVWithFirstTest(baseFolder)

            if hrv > 0:
                # print("add: " + str(epNbr))
                # print(hrv)
                if epNbr % 2 == 0:
                    even = even + 1
                    hrv_with_light.append(hrv)
                if epNbr % 2 != 0:
                    uneven = uneven + 1
                    hrv_no_light.append(hrv)

        print("Uneven:" + str(uneven))
        print("even:" + str(even))

        print("Average With light:" + str(np.average(hrv_with_light)))
        print("Average Without light:" + str(np.average(hrv_no_light)))

        return ttest_ind(hrv_no_light, hrv_with_light)

    def getHRandHRVBaseAvg(self):
        hr_base = []
        hrv_base = []

        for epNbr in self.epNbrs:
            baseFolder = self.baseFolder + "empatica_ep_" + str(epNbr).zfill(
                2) + "/splitParts/"
            hr2 = self.getBaseHR(baseFolder)
            hr2Avg = np.average(hr2['HR'])

            hrv = self.calculateHRVRMSSDforBaseIbi(baseFolder)

            if (hr2Avg > 0):
                hr_base.append(hr2Avg)
                hrv_base.append(hrv)
            #print ( "EPisode: "+ str(epNbr) + " Has HR: "+ str(hr2Avg) + " and HRV: " + str(hrv))

        hrv_no_light, hrv_with_light, even, uneven = self.getHRVRMSSDAvgsAndTTest()
        hr_no_light, hr_with_light, even1, uneven1 = self.getHRAvgAndTTest()
        print("With light hrv compared to baseline -> high p-value = Good")
        print(self.calculateTTest( hrv_with_light, hrv_base))
        print("Without light hrv compared to baseline ")
        print(self.calculateTTest( hrv_no_light, hrv_base))
        print("With light hr compared to baseline ")
        print(self.calculateTTest(hr_with_light, hr_base))
        print("Without light hr compared to baseline ")
        print(self.calculateTTest(hr_no_light, hr_base))
        printAvgMeanStdVar(hr_base, hrv_base)


