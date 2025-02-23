import matplotlib.pyplot as plt
from utilities import readEdfFile


edf_file = r"c:\Document\PhD\EEG\Artifact\data\tuh_eeg_artifact\edf\01_tcp_ar\aaaaaaju_s005_t000.edf"
signal, fileStartTime, channelNames, samplFreq = readEdfFile(edf_file)

testSignal = signal[channelNames[0]]

plt.plot(testSignal)
plt.show()