import scipy.io.wavfile as wav
from scipy import signal
import numpy as np
import peakutils
import scipy.signal as signal
from matplotlib import pyplot as plot
import matplotlib.mlab as mlab
from scipy.signal import butter, lfilter

fs, data = wav.read('sample921_clean.wav')

sf = int(fs)
print(sf)

left=data

time = 0.05
total_windows = 50
numFramesNeeded=int(np.ceil(fs*time))

overlap = int(np.ceil(fs*0.015))


frames = 0
count = 0
data_acorr = []
shiftval = 441000

index_peak1 = []
amplitude_peak1 = []
index_peak2 = []
amplitude_peak2 = []

left = np.array(left,dtype=np.float)

specdata = []
wienerdata = []
meanArray = []
absArray = []

while (count < total_windows):
	
	new_data = left[shiftval+frames:shiftval+frames+numFramesNeeded]
	absNewData = np.absolute(new_data)
	meanArray.append(sum(absNewData))
	absArray.extend(absNewData)
	frames = frames + numFramesNeeded
	count = count +1
	
totalMean = np.mean(meanArray)
print(np.mean(meanArray))
count= 0
frames = 0
totalMeanArray = []
for i in range(len(meanArray)):
	totalMeanArray.append(totalMean)
	
while ( count < total_windows):
	
	new_data = left[shiftval+frames:shiftval+frames+numFramesNeeded]
	new_data = np.array(new_data,dtype=np.float)

	specdata.extend(new_data)
	
	
	if(meanArray[count] > totalMean):
		temp_acorr = plot.acorr(new_data,maxlags=250)

		temp_acorr = np.array(temp_acorr)[1]
		
		temp_acorr = plot.acorr(new_data,maxlags=250)
	

		temp_acorr = np.array(temp_acorr)[1]
		half_temp_acorr = temp_acorr[250:]
		indexes = peakutils.peak.indexes(np.array(half_temp_acorr),thres=0.0, min_dist=10)
		index2 = indexes[0:2]
		if(index2.size):
			index_peak1.append(index2[0])
			amplitude_peak1.append(half_temp_acorr[index2[0]])
			
		else:
			index_peak1.append(500)
			amplitude_peak1.append(0)
	else:
		index_peak1.append(500)
		amplitude_peak1.append(0)

		

	frames = frames + numFramesNeeded
	count = count +1


m = min(index_peak1)
print(m)
shift = (fs*1.0)/(m*1.0)
v = (shift * 1540.0) / (4.0*10000)
print(v)

timeAxis = []
for i in range(len(specdata)):
	timeAxis.append(i/fs)

plot.clf()

plot.subplot(311)
plot.plot(timeAxis,specdata)
plot.title('Input Signal')
plot.xlabel('time')
plot.ylabel('Amplitude')
plot.tight_layout()

plot.subplot(312)
plot.plot(meanArray,'b')
plot.plot(totalMeanArray,'r')
plot.title('Mean of Absolute values of samples in a window (50ms)')
plot.xlabel('time')
plot.ylabel('Amplitude')
plot.tight_layout()

plot.subplot(313)
plot.plot(index_peak1)
plot.title('Frame Difference between peaks')
plot.xlabel('Window')
plot.ylabel('Frame Difference')
plot.tight_layout()

plot.show()




