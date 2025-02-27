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

# 设置阈值
THRESHOLD_PEAK = 100  # 峰值振幅阈值 (单位 µV)
THRESHOLD_RMS = 50  # RMS 阈值 (单位 µV)
THRESHOLD_HF_RATIO = 0.6  # 高频能量比阈值

for file in os.listdir(edfFolder):
    if file.endswith(".edf"):
        edf_file = os.path.join(edfFolder, file)
        eegSignal, fileStartTime, channelNames, samplFreq = readEdfFile(edf_file)
        print(f"Processing {file}, Sampling Frequency: {samplFreq} Hz, length: {len(eegSignal)}")
        eegSignal = np.array(eegSignal)

        for i in range(eegSignal.shape[1]):
            # ------------------ 1. 进行 STFT 变换 ------------------ #
            # f, t_stft, Zxx = signal.stft(eegSignal[:, i], samplFreq, nperseg=256, noverlap=128)
            f, t_stft, Zxx = signal.stft(eegSignal[i] , samplFreq, nperseg=256, noverlap=128)

            # 计算时频能量
            stft_power = np.abs(Zxx) ** 2

            # ------------------ 2. 伪影检测 ------------------ #
            # 设定高能量阈值（基于 STFT 计算能量）
            threshold = np.percentile(stft_power, 95)  # 设定 95% 分位数作为阈值
            artifact_mask = stft_power > threshold  # 标记高能量伪影区域
            artifact_times = t_stft[np.any(artifact_mask, axis=0)]  # 选出包含伪影的时间点
            print("Detected artifact times:", artifact_times)


            # ------------------ 3. 结果可视化 ------------------ #
            plt.figure(figsize=(12, 6))

            # # (1) 绘制原始信号
            # plt.subplot(2, 1, 1)
            # plt.plot(eegSignal, label="EEG with Artifact", color='b')
            # plt.title("ori signal")
            # plt.legend()

            # # # (2) 绘制 STFT 时频图
            # # plt.subplot(3, 1, 2)
            # # plt.pcolormesh(t_stft, f, np.log(stft_power), shading='auto', cmap='jet')
            # # plt.title("STFT 变换时频图")
            # # plt.ylabel("Frequency (Hz)")
            # # plt.colorbar()

            # # (3) 标记伪影区域
            # plt.subplot(2, 1, 2)
            plt.plot(eegSignal, color='b')
            plt.fill_between(t_stft, 0, max(f), where=np.any(artifact_mask, axis=0), color='r', alpha=0.3, label="Detected Artifact")
            plt.title("artifact area")
            plt.legend()
            plt.show()

            break
        break

            # plt.tight_layout()
            # plt.show()
