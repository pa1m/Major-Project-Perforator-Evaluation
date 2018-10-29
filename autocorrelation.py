import scipy.io.wavfile as wav
import numpy as np
import peakutils
import scipy.signal
from matplotlib import pyplot as plot
import matplotlib.mlab as mlab
from scipy.signal import butter, lfilter


def butter_lowpass(cutOff, fs, order):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='low', analog = True)
    return b, a

fs, data = wav.read('sample921_clean.wav')
sf = int(fs)
print(sf)

left=data

# for Dual Channel
#left = []
#right=[]
#for i in range (0,len(data)):
	#left.insert(i,int(data[i][0]))
	



time = 0.025
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

    
#w_left = scipy.signal.wiener(left,mysize = 10)

#scipy.io.wavfile.write('rec1wiener.wav',fs,w_left)

specdata = []
wienerdata = []

while ( count < 200):


	new_data = left[shiftval+frames:shiftval+frames+numFramesNeeded]
	new_data = np.array(new_data,dtype=np.float)

	specdata.extend(new_data)

	#wiener_data = scipy.signal.wiener(new_data,mysize = 50)

	#wienerdata.extend(wiener_data)

	temp_acorr = plot.acorr(new_data,maxlags=250)
	
	#temp_acorr = plot.acorr(wiener_data,maxlags=250)
	temp_acorr = np.array(temp_acorr)[1]

	frames = frames + numFramesNeeded
	count = count +1

	half_temp_acorr = temp_acorr[250:]
	indexes = peakutils.peak.indexes(np.array(half_temp_acorr),thres=0.0, min_dist=10)

	index2 = indexes[0:2]

	if(index2.size):
		index_peak1.append(index2[0])
		amplitude_peak1.append(half_temp_acorr[index2[0]])
		
	else:
		index_peak1.append(500)
		amplitude_peak1.append(0)


	#For Second peak
	
	#index_peak2.append(index2[1])
	#amplitude_peak2.append(half_temp_acorr[index2[1]])
	

m = min(index_peak1)
print(m)
shift = (fs*1.0)/(m*1.0)
v = (shift * 1540.0) / (4.0*10000)
print(v)



plot.clf()
plot.subplot(411)
plot.plot(specdata)


#plot.subplot(412)
##plot.title('Amplitude of peak for First Peak')
#plot.plot(specdata)
##plot.xlabel('Frames')
##plot.ylabel('Amplitude of peak for First Peak')


plot.subplot(412)
plot.specgram(x=specdata,NFFT=numFramesNeeded,  Fs=sf, noverlap=overlap, mode='psd')
plot.ylim((0,7000))



plot.subplot(413)
plot.plot(index_peak1)



plot.subplot(414)
plot.plot(amplitude_peak1)


plot.show()




