import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


colnames=['Time','IBI']
ibi = pd.read_csv('IBI.csv', names=colnames, header=0)
