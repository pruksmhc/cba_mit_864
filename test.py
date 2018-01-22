[f, fs, nbits] = wavread('input.wav');
[f2, fs2, nbits2] = wavread('input-truncated.wav');

top = 1/size(f,1)*(sum(f.^2))
bottom = 1/size(f2,1)*(sum(f2.^2))

Y = 10*log10(top/bottom)