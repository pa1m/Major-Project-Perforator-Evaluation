import scipy.io.wavfile as wav
from scipy import signal
import numpy as np
import peakutils
import scipy.signal as signal
from matplotlib import pyplot as plot
import matplotlib.mlab as mlab
from scipy.signal import butter, lfilter

def square(list):
    return [i ** 2 for i in list]

def sumlist(list1,list2):
	return [a+b for a,b in zip(list1,list2)]

fs, data = wav.read('sample921.wav')

sf = int(fs)


left=data

time = 0.05

numFramesNeeded=int(np.ceil(fs*time))

total_windows = len(left)/numFramesNeeded - 1 - 100

overlap = int(np.ceil(fs*0.015))


frames = 0
count = 0
data_acorr = []
shiftval = 220500

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
count= 0
frames = 0
totalMeanArray = []

for i in range(len(meanArray)):
	totalMeanArray.append(totalMean)

signalSpectrum = []
noiseSpectrum = []
	
while ( count < total_windows):
	
	new_data = left[shiftval+frames:shiftval+frames+numFramesNeeded]
	new_data = np.array(new_data,dtype=np.float)

	specdata.extend(new_data)
	
	if(meanArray[count] > totalMean):
		if(not len(signalSpectrum)):
			signalSpectrum.extend(square(np.absolute(np.fft.fft(new_data))))
		else:
			signalSpectrum = sumlist(signalSpectrum,square(np.absolute(np.fft.fft(new_data))))
	else:
		if(not len(noiseSpectrum)):
			noiseSpectrum.extend(square(np.absolute(np.fft.fft(new_data))))
		else:
			noiseSpectrum = sumlist(noiseSpectrum,square(np.absolute(np.fft.fft(new_data))))

	frames = frames + numFramesNeeded
	count = count +1

meanSignalSpectrum = [x/total_windows for x in signalSpectrum]
meanNoiseSpectrum  = [x/total_windows for x in noiseSpectrum]
count= 0
frames = 0
wiener_output = []

while ( count < total_windows):
	
	new_data = left[shiftval+frames:shiftval+frames+numFramesNeeded]
	new_data = np.array(new_data,dtype=np.float)
	
	spectrum_data = (np.fft.fft(new_data))

	filter_data = []
	
	for i in range(len(spectrum_data)):
		filter_data.append(spectrum_data[i]*(1.0/(1.0+(meanNoiseSpectrum[i]*1/(meanSignalSpectrum[i])))))
	
	
	wiener_output.extend(np.fft.ifft(filter_data))
	frames = frames + numFramesNeeded
	count = count +1

wiener_output = np.array(wiener_output,dtype=np.float)
print(len(wiener_output))
wav.write('filtered.wav',fs,wiener_output)

timeAxis = []
for i in range(len(specdata)):
	timeAxis.append(i/fs)

plot.clf()

plot.subplot(211)
plot.plot(timeAxis,specdata)
plot.tight_layout()
plot.title('Unfiltered Sample')


plot.subplot(212)
plot.plot(timeAxis,wiener_output)
plot.tight_layout()
plot.title('Wiener filtered Sample')

plot.show()






