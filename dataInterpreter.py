import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import HRVCalcs as hrvCalc



def calculateHRVforFirstAndSecondIbi(folder):
    colnames=['IBI','Time']
    ibi1 = pd.read_csv(folder+'1IBInoLight.csv', names=colnames, header=0)
    ibi2 = pd.read_csv(folder+'2IBIblue.csv', names=colnames, header=0)

    hrv1 = hrvCalc.calculateRMSSDFromIbi(ibi1)

    hrv2 = hrvCalc.calculateRMSSDFromIbi(ibi2)

    return hrv1,hrv2

# Calculate one ibi
epNbr = "04"
baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/empatica_ep_"+epNbr+"/splitParts/"

hrv1Calc, hrv2Calc = calculateHRVforFirstAndSecondIbi(baseFolder)
print("HRV1: " + str(hrv1Calc))
print("HRV2: " + str(hrv2Calc))
