from scipy.io import wavfile
import numpy as np
# Signal to noise ratio
# https://pdfs.semanticscholar.org/fdd7/d8dc7457fe6dc74fdfb8a1501c501605f430.pdf

def SNR(orig, est):
	return 10* np.log10((np.mean(orig**2)/np.mean((orig-est)**2)))

def distortion(orig, est):
	num = np.mean((orig - (np.mean(orig**2)/np.mean(est**2))*est)**2)
	denom = np.mean(orig**2)
	print(num)
	print(denom)
	return 10*np.log10(num/denom)

