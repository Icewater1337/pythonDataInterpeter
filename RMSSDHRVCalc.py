import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




# RMSSD Formula: sqrt( (1/N-1) * summe( RRi+1 - RRi)^2)


def calculateRMSSDFromIbi(ibi):
    rmssdSumPart = 0
    ibi = ibi['IBI']
    for x in range(ibi.size-1):
        rmssdSumPart += (ibi[x+1] - ibi[x])**2

    rmssd = np.math.sqrt((1/(ibi.size-1))*rmssdSumPart)

    return rmssd



