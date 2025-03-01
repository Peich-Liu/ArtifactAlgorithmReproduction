import numpy as np
import pandas as pd
import pyedflib
import datetime

def readEdfFile(fileName):
    ''' 
    Reads .edf file, returns signal, start time, channel names and sampling frequency
    - this need to be modified to last raw is not EEG
    - this function is assumed that every signal has same length
    '''
    #data loading
    f = pyedflib.EdfReader(fileName)
    n = f.signals_in_file
    channelNames = f.getSignalLabels()
    samplFreq =f.getSampleFrequency(0)
    fileStartTime=datetime.datetime(f.startdate_year, f.startdate_month, f.startdate_day, f.starttime_hour, f.starttime_minute, f.starttime_second, f.starttime_subsecond)
    
    #Signal formalization
    data = np.zeros((f.getNSamples()[0], n))
    for i in np.arange(n-3):
        data[:, i] = f.readSignal(i)

    # dataDF = pd.DataFrame(data.T, index=channelNames)
    dataDF=pd.DataFrame(data, columns=channelNames)
    print(dataDF)
    # print(dataDF.shape)


    return dataDF,fileStartTime, channelNames, samplFreq