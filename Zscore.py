import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore

from utilities import readEdfFile

edfFolder = r"c:\Document\PhD\EEG\Artifact\data\tuh_eeg_artifact\edf\01_tcp_ar"
threshold = 3  # Z-score 阈值 (可调整)

artifact_results = []  # 存储伪影检测结果

for file in os.listdir(edfFolder):
    if file.endswith(".edf"):
        edf_file = os.path.join(edfFolder, file)
        eegSignal, fileStartTime, channelNames, samplFreq = readEdfFile(edf_file)
        
        for column in eegSignal.columns:
            signal = eegSignal[column].values  # 获取通道信号
            window_size = int(samplFreq * 2)  # 2秒窗口
            step_size = int(samplFreq * 0.5)  # 0.5秒步长
            num_samples = len(signal)
            
            artifact_times = []  # 存储伪影时间点
            
            for start in range(0, num_samples - window_size, step_size):
                window = signal[start:start + window_size]  # 取窗口信号
                z_scores = zscore(window)  # 计算 Z-score
                artifact_indices = np.where(np.abs(z_scores) > threshold)[0]  # 找到超出阈值的点
                
                if len(artifact_indices) > 0:
                    artifact_time = (start + artifact_indices) / samplFreq  # 计算伪影发生的时间点
                    artifact_results.append({
                        'file': file,
                        'channel': column,
                        'start_time': artifact_time.min(),
                        'end_time': artifact_time.max()
                    })
                    artifact_times.extend(artifact_time)
            
            # 绘制信号和伪影检测结果
            plt.figure(figsize=(12, 4))
            plt.plot(np.arange(num_samples) / samplFreq, signal, label='EEG Signal')
            plt.scatter(artifact_times, [signal[int(t * samplFreq)] for t in artifact_times], color='red', label='Detected Artifacts', marker='x')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.title(f'Artifact Detection in {file} - {column}')
            plt.legend()
            plt.show()

# 转换为 DataFrame 以便后续分析
artifact_df = pd.DataFrame(artifact_results)
print(artifact_df.head())