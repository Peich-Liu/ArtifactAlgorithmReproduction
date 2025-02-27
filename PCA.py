import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from utilities import readEdfFile


edfFolder = r"c:\Document\PhD\EEG\Artifact\data\tuh_eeg_artifact\edf\01_tcp_ar"
for file in os.listdir(edfFolder):
    if file.endswith(".edf"):
        edf_file = os.path.join(edfFolder, file)
        signal, fileStartTime, channelNames, samplFreq = readEdfFile(edf_file)


        scaler = StandardScaler()
        # signal_scaled = scaler.fit_transform(signal)
        signal_scaled = signal


        n_components = 5  
        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(signal_scaled)
        reconstructed = pca.inverse_transform(principal_components)

        reconstruction_error = np.mean((signal_scaled - reconstructed) ** 2, axis=1)

        threshold = np.mean(reconstruction_error) + 3 * np.std(reconstruction_error)
        anomalies = reconstruction_error > threshold

        plt.figure(figsize=(12, 6))
        plt.plot(reconstruction_error, label='Reconstruction Error')
        plt.axhline(threshold, color='r', linestyle='--', label='Threshold')
        plt.scatter(np.where(anomalies)[0], reconstruction_error[anomalies], color='red', label='Detected Artifacts')
        plt.xlabel('Time Index')
        plt.ylabel('Reconstruction Error')
        plt.legend()
        plt.title('PCA-Based Artifact Detection')
        plt.show()

        print(f"Detected {np.sum(anomalies)} artifacts at indices: {np.where(anomalies)[0]}")

        break