#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the transmitter dummy for the optical communications
test and interact with it.
"""

import os
import sys

import PySimpleGUI as sg


def main():
    """Main function to start the execution of the transmitter program."""

    sending_message = False
    window = define_gui_layout()

    while True:  # Event Loop
        event, values = window.read(timeout=1)
        # print(event, values)
        if event == sg.WIN_CLOSED or event == "-EXIT-":
            break

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            base_folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(base_folder)  # get list of files in folder
            except FileNotFoundError:
                file_list = []
            file_names = [
                file_name
                for file_name in file_list
                if os.path.isfile(os.path.join(base_folder, file_name))
            ]
            window["-FILE LIST-"].update(file_names)

        if event == "-SEND-":
            sending_message = True

        if event == "-STOP-":
            sending_message = False

        if sending_message:
            # ToDo: Enviar los datos a la función de encriptado

            params = [
                values["-PARAM-FREQUENCY-"],
                values["-PARAM-DUTY_CYCLE-"],
            ]

            if values["-TOGGLE SEC1-RADIO-"]:
                print([values["-MESSAGE-"], params])

            elif values["-TOGGLE SEC2-RADIO-"]:
                file_path = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    data = file.read()
                    file.close()
                    print([data, params])

            else:
                sys.exit("Error: Algo raro ha pasado!")

        if event.startswith("-TOGGLE SEC"):
            window["-SEC1-"].update(visible=values["-TOGGLE SEC1-RADIO-"])
            window["-SEC2-"].update(visible=values["-TOGGLE SEC2-RADIO-"])

    window.close()


def define_gui_layout():
    """GUI layout"""

    # section1 = [
    #     [sg.Text("Mensaje:")],
    #     [sg.Multiline(size=(50, 10), key="-MESSAGE-")],
    # ]

    section2 = [
        [
            sg.Text("Archivo:"),
            sg.In(size=30, enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [sg.Listbox(values=[], enable_events=True, size=(50, 10), key="-FILE LIST-")],
    ]

    parameters = [
        [
            sg.Text("Frecuencia:"),
            sg.In(default_text="30", size=5, key="-PARAM-FREQUENCY-"),
            sg.Text("KHz"),
        ],
        [
            sg.Text("Duty cycle:"),
            sg.In(default_text="65", size=5, key="-PARAM-DUTY_CYCLE-"),
            sg.Text("%"),
        ],
    ]

    buttons = [
        [
            sg.Button("Enviar", key="-SEND-"),
            sg.Button("Parar", key="-STOP-"),
            sg.Button("Salir", key="-EXIT-"),
        ]
    ]

    layout = [
        [sg.Text("Emisor")],
        [
            sg.Radio(
                " Texto plano",
                "Radio",
                default=True,
                enable_events=True,
                key="-TOGGLE SEC1-RADIO-",
            ),
            sg.Radio(
                " Archivo", "Radio", enable_events=True, key="-TOGGLE SEC2-RADIO-"
            ),
        ],
        [
            # sg.Column(section1, key="-SEC1-"),
            sg.Column(section2, key="-SEC2-", visible=False),
        ],
        [
            sg.Column(parameters),
            sg.Column(buttons),
        ],
    ]

    window = sg.Window("Emisor", layout)
    return window


if __name__ == "__main__":
    main()
