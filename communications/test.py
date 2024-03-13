from scikits.audiolab import wavread
x, fs, nbits = scikits.audiolab.wavread('schubert.wav')
scikits.audiolab.play(x, fs)
N = 4*fs    # four seconds of audio
X = scipy.fft(x[:N])
Xdb = 20*scipy.log10(scipy.absolute(X))
f = scipy.linspace(0, fs, N, endpoint=False)
pylab.plot(f, Xdb)
pylab.xlim(0, 5000)   # view up to 5 kHz

Y = X*H
y = scipy.real(scipy.ifft(Y))