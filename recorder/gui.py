import PySimpleGUI as sg


AppFont = "Any 16"
sg.theme("Black")
CanvasSizeWH = 500

layout = [
    [sg.Canvas(key="-CANVAS-")],
    [
        sg.Button("Listen", font=AppFont),
        sg.Button("Stop", font=AppFont, disabled=True),
        sg.Button("Exit", font=AppFont),
    ],
    [
        sg.Slider(
            range=(0, 1),
            default_value=0.5,
            expand_x=True,
            enable_events=True,
            orientation="horizontal",
            key="-VOL-",
        )
    ],
]

window = sg.Window("Pyaudio Wave plot + FFT", layout, finalize=True)
