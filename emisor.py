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
                values["-PARAM-EXP_ID-"],
                values["-PARAM-SENDER_ANGLE-"],
                values["-PARAM-LED_POWER-"],
                values["-PARAM-BLINKING_FREQUENCY-"],
                values["-PARAM-DUMMY_DISTANCE-"],
            ]

            if values["-TOGGLE SEC_PTEXT-RADIO-"]:
                print([values["-MESSAGE-"], params])

            elif values["-TOGGLE SEC_FILE-RADIO-"]:
                file_path = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    data = file.read()
                    file.close()
                    print([data, params])
            # elif values["-TOGGLE SEC_EXP-RADIO-"]:

            else:
                sys.exit("Error: Algo raro ha pasado!")

        if event.startswith("-TOGGLE SEC"):
            window["-SEC_PTEXT-"].update(visible=values["-TOGGLE SEC_PTEXT-RADIO-"])
            window["-SEC_FILE-"].update(visible=values["-TOGGLE SEC_FILE-RADIO-"])
            window["-SEC_EXP-"].update(visible=values["-TOGGLE SEC_EXP-RADIO-"])

    window.close()


def define_gui_layout():
    """GUI layout"""

    sectionPText = [
        [sg.Text("Mensaje:")],
        [sg.Multiline(size=(50, 10), key="-MESSAGE-")],
    ]

    sectionFile = [
        [
            sg.Text("Archivo:"),
            sg.In(size=30, enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [sg.Listbox(values=[], enable_events=True, size=(50, 10), key="-FILE LIST-")],
    ]

    exp_param_input = [
        [
            sg.In(default_text="12345678", size=10, key="-PARAM-EXP_ID-"),
        ],
        [
            sg.In(default_text="45", size=5, key="-PARAM-SENDER_ANGLE-"),
            sg.Text("º"),
        ],
        [
            sg.In(default_text="1", size=5, key="-PARAM-LED_POWER-"),
            sg.Text("A"),
        ],
        [
            sg.In(default_text="30", size=5, key="-PARAM-BLINKING_FREQUENCY-"),
            sg.Text("kbps"),
        ],
        [
            sg.In(default_text="42", size=5, key="-PARAM-DUMMY_DISTANCE-"),
            sg.Text("<unit>"),
        ],
    ]
    exp_param_labels = [
        [
            sg.Text("Experiment Id:",expand_x=True),
        ],
        [
            sg.Text("Sender angle:",expand_x=True),
        ],
        [
            sg.Text("Led Power:",expand_x=True),
        ],
        [
            sg.Text("Blinking frecuency:",expand_x=True),
        ],
        [
            sg.Text("Dummy distance:",expand_x=True),
        ],
    ]
    sectionExperiment = [
        [
            sg.Column(exp_param_labels),
            sg.Column(exp_param_input),
        ]
    ]

    buttons = [
        [
            sg.Button("Execute experiment", key="-SEND-", expand_x=True),
            # sg.Button("Parar", key="-STOP-"),
            # sg.Button("Salir", key="-EXIT-"),
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
                key="-TOGGLE SEC_PTEXT-RADIO-",
            ),
            sg.Radio(
                " Archivo", "Radio", enable_events=True, key="-TOGGLE SEC_FILE-RADIO-"
            ),
            sg.Radio(
                " Experimento", "Radio", enable_events=True, key="-TOGGLE SEC_EXP-RADIO-"
            ),
        ],
        [
            sg.Column(sectionPText, key="-SEC_PTEXT-"),
            sg.Column(sectionFile, key="-SEC_FILE-", visible=False),
            sg.Column(sectionExperiment, key="-SEC_EXP-", visible=False),
        ],
        # [
        #     sg.Column(exp_param_labels),
        #     sg.Column(exp_param_input),
        # ],
        [
            sg.Column(buttons,expand_x=True),
        ],
    ]

    window = sg.Window("Emisor", layout)
    return window


if __name__ == "__main__":
    main()
