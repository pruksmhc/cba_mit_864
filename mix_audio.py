
def mix_audio(s1, s2):
	# Concaenate, then applymixing matrix
	sample = np.c_[voice_1, voice_2]
	A = np.array([[1, 0.5], [0.5, 1]])
	X = np.dot(sample, A)
	# Output: 2 rows, each row being a different source. 
	return X