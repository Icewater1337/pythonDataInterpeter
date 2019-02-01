import numpy as np
import pandas as pd


def readFiles(fname):
    dict = {}
    dict['IBI'] = readIBI(fname)
    dict['BVP'] = readBvp(fname)
    dict['EDA'] = readEda(fname)
    dict['Temp'] = readTemperature(fname)
    dict['HR'] = readHr(fname)

    return dict



def readBvp(fname):
    #Photoplethysmograph data (not really interpretable)
    bvp = pd.read_csv(fname +'/BVP.csv',header=None)
    bvp_rate=bvp.iloc[1,0]
    bvp_start=bvp.iloc[0,0]
    bvp=bvp.drop([bvp.index[1],bvp.index[0]], axis=0)
    bvp=bvp.set_index(np.arange(bvp_start, bvp_start+len(bvp)*(1.0/bvp_rate),1.0/bvp_rate))
    bvp.columns=['bvp']

    return bvp

def readEda(fname):
    #Electrodermal activity sensor expressed as microsiemens (μS)
    eda = pd.read_csv(fname +'/EDA.csv',header=None)
    eda_rate=eda.iloc[1,0]
    eda_start=eda.iloc[0,0]
    eda=eda.drop([eda.index[1],eda.index[0]],axis=0)
    eda=eda.set_index(np.arange(eda_start, eda_start+len(eda)*(1.0/eda_rate),1.0/eda_rate))
    eda.columns=['eda']
    return eda

def readTemperature(fname):
    #Temperature in degrees
    temp = pd.read_csv(fname +'/TEMP.csv',header=None)
    temp_rate=temp.iloc[1,0]
    temp_start=temp.iloc[0,0]
    temp=temp.drop([temp.index[1],temp.index[0]],axis=0)
    temp=temp.set_index(np.arange(temp_start, temp_start+len(temp)*(1.0/temp_rate),1.0/temp_rate))
    temp.columns=['temp']
    return temp

def readHr(fname):
    #Average heart rate extracted from the BVP signal
    hr = pd.read_csv(fname +'/HR.csv',header=None)
    hr_rate=hr.iloc[1,0]
    hr_start=hr.iloc[0,0]
    hr=hr.drop([hr.index[1],hr.index[0]],axis=0)
    hr=hr.set_index(np.arange(hr_start, hr_start+len(hr)*(1.0/hr_rate),1.0/hr_rate))
    hr.columns=['hr']
    return hr

def readIBI(fname):
    ibi = pd.read_csv(fname+ '/IBI.csv', header=None)
    ibi_start = ibi.iloc[0,0]
    ibi_first = ibi.iloc[1,0]
    ibi_times = ibi.iloc[1:,0]
    ibi = ibi.drop([0], axis=1)
    ibi = ibi.drop([0], axis=0)
    ibi.columns=['ibi']

    ibi_indices = []
    for idx in range(ibi_times.size):
        ibi_indices.append(ibi_start+ibi_times.iloc[idx])

    ibi = ibi.set_index(np.asarray(ibi_indices))
    return ibi


    #HRV
    #hrv = pd.read_csv(fname +'/HRV.csv',header=True)
    #hrv_rate=hrv.iloc[1,0]
    #hrv_start=hrv.iloc[0,0]
    #hrv=hrv.drop([hr.index[1],hrv.index[0]],axis=0)
    #hrv=hrv.set_index(np.arange(hrv_start, hrv_start+len(hrv)*(1.0/hrv_rate),1.0/hrv_rate))
    #hrv.columns=['hrv']


   # emp_currdata=pd.merge(pd.merge(bvp,hr,left_index=True,right_index=True,how='outer'),pd.merge(eda,temp,left_index=True,right_index=True,how='outer'),left_index=True,right_index=True,how='outer')
    #emp_currdata = pd.merge(emp_currdata, hrv, left_index=True, right_index=True,how='outer')
    #print(emp_currdata)

    #return emp_currdata

#fname = "C:/Users/Icewater/Desktop/masterThesisPrograms/pythonDataInterpeter"

#readFiles(fname)