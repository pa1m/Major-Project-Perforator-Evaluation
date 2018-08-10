

#Python Code to create a Short term Spectrogram of a wave

import scipy.io.wavfile as wav
import numpy as np
from matplotlib import pyplot as plot

fs, data = wav.read('sample.wav')
sf = int(fs)

#Getting only the left Stereo from a dual channel Wave
left=[]
for i in range (0,len(data)):
	left.insert(i,int(data[i][0]))
	
#Getting only the right Stereo from a dual channel Wave
right=[]
for i in range (0,len(data)):
	right.insert(i,int(data[i][1]))

time = 0.025
numFramesNeeded=int(np.ceil(fs*time))

overlap = int(np.ceil(fs*0.015))

# Plot the signal read from wav file

plot.subplot(411)

plot.title('Spectrogram of a wav file')

 

plot.plot(left)

plot.xlabel('Sample')

plot.ylabel('Amplitude')




plot.subplot(412)

plot.specgram(x=left,NFFT=numFramesNeeded,  Fs=sf, noverlap=overlap)

plot.xlabel('Time')

plot.ylabel('Frequency')



plot.subplot(413)

plot.specgram(x=right,NFFT=numFramesNeeded,  Fs=sf, noverlap=overlap)

plot.xlabel('Time')

plot.ylabel('Frequency')

plot.subplot(414)
plot.plot(right)

plot.xlabel('Sample')

plot.ylabel('Amplitude')



plot.show()
