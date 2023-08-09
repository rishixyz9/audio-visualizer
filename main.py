from recorder.recorder import Recorder
from recorder.gui import window
from scraper.stream import getWav
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use('TkAgg')

fig, ax = plt.subplots()
ax.plot(([0], [0]))

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

getWav("https://www.youtube.com/watch?v=mq7T8c8YsdU&ab_channel=MemSound")

aud_in = Recorder('audio.wav')
listening = False

while True:
    event, values = window.read(timeout=.5)
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        aud_in.stop()
        aud_in.close()
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