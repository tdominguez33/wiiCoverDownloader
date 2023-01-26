import PySimpleGUI as sg
import main
import threading

def gui():
    global window
    # Define the window's contents
    layout = [[sg.Text("ID of the Game to download the Cover:")],
            [sg.Input(key='-INPUT-')],
            [sg.Button('Download')],
            [sg.Output(key = '-Console-', size=(70, 12))],
            [sg.Button('Download ALL'), sg.Button('Quit')]]

    # Create the window
    window = sg.Window('Wii Cover Downloader', layout)


    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read(timeout=100)
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        # Output a message to the window
        if event == 'Download' and values['-INPUT-'] != '':
            threading.Thread(target = main.getCover, args = (values['-INPUT-'],), daemon = True).start()
        
        if event == 'Download ALL':
            threading.Thread(target = main.downloadAll, args=(), daemon=True).start()

    window.close()

gui()
