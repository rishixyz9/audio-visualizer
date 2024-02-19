import sys

sys.path.append("../")

from recorder.gui import window
import PySimpleGUI as sg
import asyncio
import websockets
import json

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use("TkAgg")

fig, ax = plt.subplots()


def draw_figure(canvas, figure):
    tkcanvas = FigureCanvasTkAgg(figure, canvas)
    tkcanvas.draw()
    tkcanvas.get_tk_widget().pack(side="top", fill="both", expand=1)
    return tkcanvas


def update_plot(canvas, data):
    # Clear the current axes
    ax.clear()

    # Given your data structure, you might need to adjust the width for the bars to properly display them
    ax.bar(
        [i + 1 for i in range(len(data[0]))], data[1], width=1, align="center"
    )  # Plot the bar graph with data

    # It's often helpful to set the x-axis to a logarithmic scale for frequency data

    # Optionally set labels for clarity
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Frequency Spectrum")

    # Update the canvas
    canvas.draw_idle()


tkcanvas = draw_figure(window["-CANVAS-"].TKCanvas, fig)


async def gui():
    listening = False
    while True:
        websocket = await websockets.connect("ws://localhost:8765")
        event, values = window.read(timeout=0.25)
        if event == sg.WIN_CLOSED or event == "Exit":
            await websocket.send("exit")
            await websocket.close()
            break
        if event == "Listen":
            window.FindElement("Stop").Update(disabled=False)
            window.FindElement("Listen").Update(disabled=True)
            listening = True
            await websocket.send("play")

        if event == "Stop":
            listening = False
            window.FindElement("Stop").Update(disabled=True)
            window.FindElement("Listen").Update(disabled=False)
            await websocket.send("stop")

        if event == "-VOL-":
            await websocket.send("Vol")
            await websocket.send(str(values["-VOL-"]))

        if listening:
            await websocket.send("play")
            data = json.loads(await websocket.recv())
            update_plot(tkcanvas, data)

        await websocket.close()


asyncio.run(gui())
