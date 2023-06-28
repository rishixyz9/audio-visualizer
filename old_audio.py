import pyaudio
import soundfile as sf
import PySimpleGUI as sg
import numpy as np

OUTPUT_FILE_NAME = "out.wav"    # file name.
SAMPLE_RATE = 44100              # [Hz]. sampling rate.
RECORD_SEC = 5                  # [sec]. duration recording audio.


AppFont = 'Any 16'
sg.theme('Black')
CanvasSizeWH = 500

layout = [[sg.Graph(canvas_size=(CanvasSizeWH, CanvasSizeWH),
                    graph_bottom_left=(-16, -16),
                    graph_top_right=(116, 116),
                    background_color='#B9B9B9',
                    key='graph')],
          [sg.ProgressBar(4000, orientation='h',
                          size=(20, 20), key='-PROG-')],
          [sg.Button('Listen', font=AppFont),
           sg.Button('Stop', font=AppFont, disabled=True),
           sg.Button('Exit', font=AppFont)]]

window = sg.Window('Pyaudio Wave plot + FFT', layout, finalize=True)
p = pyaudio.PyAudio()
buffer = ""

frames = np.array([], dtype=np.int16)

stream = False

def callback(in_data, frame_count, time_info, status):
    buffer = np.frombuffer(in_data, dtype=np.int16)
    global frames
    frames = np.concatenate((frames, buffer))
    return (in_data, pyaudio.paContinue)


def listen():
    window.FindElement('Stop').Update(disabled=False)
    window.FindElement('Listen').Update(disabled=True)
    global stream
    stream =  p.open(format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=128,
            stream_callback=callback)
    stream.start_stream()

def stop():
    if stream:
        stream.stop_stream()
        stream.close()
        window.FindElement('Stop').Update(disabled=True)
        window.FindElement('Listen').Update(disabled=False)


while True:
    event, values = window.read(timeout=1)
    if event == sg.WIN_CLOSED or event == 'Exit':
        stop()
        p.terminate()
        break
    if event == 'Listen':
        listen()
    if event == 'Stop':
        stop()

print(frames)

# frames *= 10

sf.write(file=OUTPUT_FILE_NAME, data=frames, samplerate=SAMPLE_RATE)