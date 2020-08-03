# img_viewer.py

import PySimpleGUI as sg
import os.path
import threading

from observer.dir_monitor import CreateObserverDir
from observer.dir_monitor import *



# For now will only show the name of the file that was chosen
folder_path_column = [
    [
        sg.Text("Monitor Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [sg.Text("Choose an folder from browse:")],
    #[sg.Listbox(df['result'],size(70,20),key='-OUT-')]
    [sg.Output(size=(80, 30))],
]


# First the window layout in 2 columns
log_list_column = [
    

          [sg.Text('Long task to perform example')],
          [sg.Output(size=(70, 12))],

]


# ----- Full layout -----
layout = [
    [
        sg.Column(folder_path_column),
        #sg.VSeperator(),
        #sg.Column(log_list_column),
    ]
]

def observer(_path):
    t = CreateObserverDir(_path)
    t.run()

def _event_(event, values):
    # Folder name was filled in, make a list of files in the folder
    if event.startswith('-FOLDER-'):
        folder = values["-FOLDER-"]
        try:
            threading.Thread(target=observer, args=(folder,), daemon=True).start()
            # Get list of files in folder
        except Exception as e:
            print(e)

        #window["-FOLDER-"].update(fnames)
        #window["-TOUT-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = values["-FILE LIST-"]
            #print(filename)
            #window["-TOUT-"].update(filename)

        except:
            pass
    


def run():
    window = sg.Window("Image Viewer", layout)

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        _event_(event, values)
    
    window.close()



   

