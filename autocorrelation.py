import scipy.io.wavfile as wav
import numpy as np
import peakutils
import scipy.signal
from matplotlib import pyplot as plot
import matplotlib.mlab as mlab


fs, data = wav.read('sample.wav')
sf = int(fs)
left=[]
for i in range (0,len(data)):
	left.insert(i,int(data[i][0]))

time = 0.025
numFramesNeeded=int(np.ceil(fs*time))

overlap = int(np.ceil(fs*0.015))

print(fs)
print(np.ceil(fs*time))
print ((numFramesNeeded))
print(len(left))

frames = 0
count = 0
data_acorr = []
shiftval = 250000

index_peak1 = []
amplitude_peak1 = []
index_peak2 = []
amplitude_peak2 = []

specdata = []

while ( count < 1):
	
	new_data = left[shiftval+frames:shiftval+frames+numFramesNeeded]
	new_data = np.array(new_data,dtype=np.float)

	specdata.extend(new_data)
	
	temp_acorr = plot.acorr(new_data,maxlags=500)
	temp_acorr = np.array(temp_acorr)[1]

	frames = frames + numFramesNeeded
	count = count +1

	half_temp_acorr = temp_acorr[500:]
	indexes = peakutils.peak.indexes(np.array(half_temp_acorr),thres=-0.2, min_dist=10)
	
	index2 = indexes[0:2]
	
	index_peak1.append(index2[0])
	amplitude_peak1.append(half_temp_acorr[index2[0]])
	
	index_peak2.append(index2[1])
	amplitude_peak2.append(half_temp_acorr[index2[1]])
	
	
	
	



#for i in range (0,len(data_acorr)):
	#if(data_acorr[i] < 0):
		#left.insert(i,0)
	#else:
		#left.insert(i,(data_acorr[i]))
	
#print(specdata)


print(max(index_peak1))
print(min(index_peak1))

plot.clf()
#plot.subplot(211)
#plot.title('Frame Difference b/w Zeroth Peak and First peak')
plot.plot(temp_acorr)
#plot.xlabel('Frames')
#plot.ylabel('Frame Difference for First Peak')

#plot.subplot(212)
#plot.title('Amplitude of peak for First Peak')
#plot.plot(amplitude_peak1)
#plot.xlabel('Frames')
#plot.ylabel('Amplitude of peak for First Peak')


##plot.subplot(413)

##Pxx, freq, t = mlab.specgram(x=specdata,NFFT=numFramesNeeded,  Fs=sf, noverlap=overlap)
#plot.subplot(413)
#plot.specgram(x=left,NFFT=numFramesNeeded,  Fs=sf, noverlap=overlap, mode='psd')
##ha.set_yscale('log')


##plot.xlabel('Time')

##plot.ylabel('Frequency')

##plot.subplot(413)
##plot.title('Frame Difference b/w Zeroth Peak and Second peak')
##plot.plot(index_peak2)

##plot.xlabel('Frames')
##plot.ylabel('Frame Difference for Second Peak')

#plot.subplot(414)
##plot.title('Amplitude of peak for Second Peak')
#plot.plot(specdata)

##plot.xlabel('Frames')
##plot.ylabel('Amplitude of peak for Second Peak')

##plot.subplot(212)
##plot.plot(left)
plot.show()




