import numpy as np
import scipy
import matplotlib.pyplot as plt
from recorder import Recorder
from gui import window
import PySimpleGUI as sg

aud_in = Recorder('output.wav')

while True:
    event, values = window.read(timeout=1)
    if event == sg.WIN_CLOSED or event == 'Exit':
        aud_in.stop()
        aud_in.writeAudio('abc.wav')
        break
    if event == 'Listen':
        window.FindElement('Stop').Update(disabled=False)
        window.FindElement('Listen').Update(disabled=True)
        aud_in.play()
    if event == 'Stop':
        aud_in.stop()
        window.FindElement('Stop').Update(disabled=True)
        window.FindElement('Listen').Update(disabled=False)


# rate, data = scipy.io.wavfile.read('./output.wav')

# file = open('output.txt', 'w')

# print(data)

# file.write(data)

# file.close()

# data = np.fft.fft(data)

# N = len(data)    # Number of samples
# T = 1/128 # Period
# y_freq = data
# domain = len(y_freq) // 2
# x_freq = np.linspace(0, 128//2, N//2)
# plt.plot(x_freq, abs(y_freq[:domain]))
# plt.xlabel("Frequency [Hz]")
# plt.ylabel("Frequency Amplitude |X(t)|")
# plt.show()


# ff = ffmpy.FFmpeg(
#     inputs={'water.mp3': None},
#     outputs={'output.wav': None}
# )
# ff.run()

