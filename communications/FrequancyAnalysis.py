import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import *
from scipy.io import wavfile

from scipy.signal import find_peaks_cwt


from scipy.signal import find_peaks
def freq(file, start_time, end_time):

    # Open the file and convert to mono
    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Return a slice of the data from start_time to end_time
    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]

    # Fourier Transform
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)

    # Uncomment these to see the frequency spectrum as a plot
    data = np.abs(yf)
    fig = plt.plot(xf, data)
    peaks = find_peaks_cwt(data, widths=np.ones(data.shape)*2)-1
    plt.plot(data)
    plt.plot(peaks, data[peaks], "x")
    plt.show()
   
    
    lst = data
    largest = lst[0]
    list1  = xf
    #traverse the array
    for i in lst:
        if i>largest:
            largest = i

    for j in range(len(lst)):
        if lst[j] == largest:

            return list1[j]

    #peaks, _ = find_peaks(xf, height=2000)
    #print(data)
    # If we haven't already shown or saved the plot, then we need to
    # draw the figure first...
    #fig.canvas.draw()

    # Now we can save it to a numpy array.
    #data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    #data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    #print(data)
    # Get the most dominant frequency and return it
    #idx = np.argmax(np.abs(yf))
    #freq = xf[idx]
    #return freq
print (freq('audio.wav',0,1))
