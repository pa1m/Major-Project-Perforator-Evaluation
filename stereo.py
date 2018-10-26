import scipy.io.wavfile as wav
import numpy as np
import peakutils
import scipy.signal
from matplotlib import pyplot as plot

fs, data = wav.read('sample.wav')
sf = int(fs)
left=[]
right=[]
for i in range (0,len(data)):
	left.insert(i,int(data[i][0]))
	right.insert(i,int(data[i][1]))
	
plot.subplot(211)
plot.plot(left, color='g')
plot.plot(right,color = 'b')

fs, data = wav.read('rec1.wav')
sf = int(fs)
left=[]
right=[]
for i in range (0,len(data)):
	left.insert(i,int(data[i][0]))
	right.insert(i,int(data[i][1]))
	
plot.subplot(212)
plot.plot(left, color='g')
plot.plot(right,color = 'b')

plot.show()
