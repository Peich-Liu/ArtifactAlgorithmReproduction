import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from scipy.signal import butter, filtfilt
from sklearn.decomposition import FastICA
from utilities import readEdfFile
import scipy.signal as signal

edfFolder = r"c:\Document\PhD\EEG\Artifact\data\tuh_eeg_artifact\edf\01_tcp_ar"

for file in os.listdir(edfFolder):
    if file.endswith(".edf"):
        edf_file = os.path.join(edfFolder, file)
        eegSignal, fileStartTime, channelNames, samplFreq = readEdfFile(edf_file)
        print(f"Processing {file}, Sampling Frequency: {samplFreq} Hz, length: {len(eegSignal)}")
        # eegSignal = np.array(eegSignal)

        # for i in range(eegSignal.shape[1]):
        for column in eegSignal.columns:
            print(f"Processing {column}")

            f, t_stft, Zxx = signal.stft(eegSignal[column], samplFreq, nperseg=256, noverlap=128)
            stft_power = np.abs(Zxx) ** 2

            threshold = np.percentile(stft_power, 95)  # 设定 95% 分位数作为阈值
            artifact_mask = stft_power > threshold  # 标记高能量伪影区域
            artifact_times = t_stft[np.any(artifact_mask, axis=0)]  # 选出包含伪影的时间点
            print("Detected artifact times:", artifact_times)

            plt.figure(figsize=(12, 6))
            plt.plot(eegSignal[column], color='b')
            plt.fill_between(t_stft, 0, max(f), where=np.any(artifact_mask, axis=0), color='r', alpha=0.3, label="Detected Artifact")
            plt.title("artifact area")
            plt.legend()
            plt.show()
        break
