import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore

from utilities import readEdfFile


edfFolder = r"c:\Document\PhD\EEG\Artifact\data\tuh_eeg_artifact\edf\01_tcp_ar"
for file in os.listdir(edfFolder):
    if file.endswith(".edf"):
        edf_file = os.path.join(edfFolder, file)
        eegSignal, fileStartTime, channelNames, samplFreq = readEdfFile(edf_file)

        for column in eegSignal.columns:
            signal = eegSignal[column].values 
            window_size = int(samplFreq * 2)  
            step_size = int(samplFreq * 0.5)  


            X = np.array([signal[i:i+window_size] for i in range(0, len(signal) - window_size, step_size)])

            if X.shape[0] < 2 or X.shape[1] < 2:
                print(f"Skipping channel {column} due to insufficient data.")
                continue

            pca = PCA(n_components=1)
            principal_components = pca.fit_transform(X).flatten()
            threshold = 3  
            anomaly_indices = np.where(np.abs(zscore(principal_components)) > threshold)[0]
            artifact_positions = [i * step_size for i in anomaly_indices]

            plt.figure(figsize=(10, 4))
            plt.plot(signal, label=f"{column} Original Signal")
            plt.scatter(artifact_positions, signal[artifact_positions], color='red', label="Detected Artifacts", marker='o')
            plt.legend()
            plt.title(f"Artifact Detection in {column} - {file}")
            plt.xlabel("Time (samples)")
            plt.ylabel("Amplitude")
            plt.show()

            break