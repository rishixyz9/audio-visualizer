import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to generate/update the matplotlib plot
def update_plot(canvas, data):
    plt.cla()  # Clear previous plot
    # Update your matplotlib plot here using 'data'
    plt.plot(data)
    canvas.draw()

# PySimpleGUI window layout
layout = [[sg.Canvas(size=(400, 300), key='-CANVAS-')],
          [sg.Button('Update Plot'), sg.Button('Exit')]]

# Create the window
window = sg.Window('Real-Time Matplotlib Plot', layout, finalize=True)

# Generate initial data for the plot (e.g., list of numbers)
initial_data = [1, 2, 3, 4, 5]

# Create the initial matplotlib plot
fig, ax = plt.subplots()
ax.plot(initial_data)
canvas = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Update Plot':
        # Update the data for the plot (e.g., get new data from a source)
        new_data = [i + 1 for i in initial_data]
        initial_data = new_data  # Update the initial data for the next iteration
        update_plot(canvas, new_data)

window.close()
