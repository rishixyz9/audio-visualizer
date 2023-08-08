from recorder import Recorder
from gui import window
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

aud_in = Recorder()
listening = False

data = ([0], [0])

fig, ax = plt.subplots()
ax.plot(data)

def draw_figure(canvas, figure):
   tkcanvas = FigureCanvasTkAgg(figure, canvas)
   tkcanvas.draw()
   tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)
   return tkcanvas

def update_plot(canvas, data):
    
    plt.cla()
    plt.plot(data[0], data[1])
    plt.xlim(0, 2000)
    canvas.draw()

tkcanvas = draw_figure(window['-CANVAS-'].TKCanvas, fig)

# a._label("Frequency [Hz]")
# a._label("Frequency Amplitude |X(t)|")

while True:
    event, values = window.read(timeout=1)
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        aud_in.stop()
        aud_in.writeAudio('abc.wav')
        break
    if event == 'Listen':
        window.FindElement('Stop').Update(disabled=False)
        window.FindElement('Listen').Update(disabled=True)
        listening = True
    if event == 'Stop':
        aud_in.stop()
        listening = False
        window.FindElement('Stop').Update(disabled=True)
        window.FindElement('Listen').Update(disabled=False)

    if(listening):
        data = aud_in.play()
        update_plot(tkcanvas, data)

    



# import pyaudio
# import wave

# # the file name output you want to record into
# filename = "recorded.wav"
# # set the chunk size of 1024 samples
# chunk = 1024
# # sample format
# FORMAT = pyaudio.paInt16
# # mono, change to 2 if you want stereo
# channels = 1
# # 44100 samples per second
# sample_rate = 44100
# record_seconds = 5
# # initialize PyAudio object
# p = pyaudio.PyAudio()
# # open stream object as input & output
# stream = p.open(format=FORMAT,
#                 channels=channels,
#                 rate=sample_rate,
#                 input=True,
#                 output=True,
#                 frames_per_buffer=chunk)
# frames = []
# print("Recording...")
# for i in range(int(sample_rate / chunk * record_seconds)):
#     data = stream.read(chunk)
#     # if you want to hear your voice while recording
#     # stream.write(data)
#     frames.append(data)
# print("Finished recording.")
# # stop and close stream
# stream.stop_stream()
# stream.close()
# # terminate pyaudio object
# p.terminate()
# # save audio file
# # open the file in 'write bytes' mode
# wf = wave.open(filename, "wb")
# # set the channels
# wf.setnchannels(channels)
# # set the sample format
# wf.setsampwidth(p.get_sample_size(FORMAT))
# # set the sample rate
# wf.setframerate(sample_rate)
# # write the frames as bytes
# wf.writeframes(b"".join(frames))
# # close the file
# wf.close()