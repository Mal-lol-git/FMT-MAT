# img_viewer.py

import PySimpleGUI as sg
import os.path
import threading

from observer.dir_monitor import CreateObserverDir
from observer.dir_monitor import *


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



log_list_column = [
    

          [sg.Text('Long task to perform example')],
          [sg.Output(size=(70, 12))],

]



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
    if event.startswith('-FOLDER-'):
        folder = values["-FOLDER-"]
        try:
            threading.Thread(target=observer, args=(folder,), daemon=True).start()

        except Exception as e:
            print(e)

    elif event == "-FILE LIST-":  
        try:
            filename = values["-FILE LIST-"]

        except:
            pass
    


def run():
    window = sg.Window("Image Viewer", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        _event_(event, values)
    
    window.close()



   

