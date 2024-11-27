#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the receiver dummy for the optical communications test
and interact with it.
"""

import os
import sys

import PySimpleGUI as sg


def main():
    """Main function to start the execution of the receiver program."""

    folder = None
    receiving_message = False
    window = define_gui_layout()

    while True:  # Event Loop
        event, values = window.read(timeout=1)
        # print(event, values)
        if event == sg.WIN_CLOSED or event.startswith("-EXIT"):
            break

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]

        if event == "-SAVE-":
            if not os.path.isdir(folder):
                window["-PATH-ERROR-MSG-"].update(visible=True)

            else:
                window["-PATH-ERROR-MSG-"].update(visible=False)
                file_path = os.path.join(folder, values["-FILE_NAME-"])

                # ToDo: Guardar datos al archivo
                print(file_path)

        if event == "-START-":
            receiving_message = True

        if event == "-STOP-":
            receiving_message = False

        if event == "-CLEAN-":
            window["-MESSAGE-"].update(value="")

        if values["-TOGGLE SEC1-RADIO-"] and receiving_message:
            # ToDo: Recibir los datos de la función de desencriptado

            window["-MESSAGE-"].update(
                value=values["-MESSAGE-"] + "\nHello world!\nHola mundi!\n..."
            )
            #! Salto de línea no reconocido

        if event.startswith("-TOGGLE SEC"):
            window["-SEC1-"].update(visible=values["-TOGGLE SEC1-RADIO-"])
            window["-SEC2-"].update(visible=values["-TOGGLE SEC2-RADIO-"])

    window.close()


def define_gui_layout():
    """GUI layout"""

    section1 = [
        [sg.Text("Mensaje:")],
        [sg.Multiline(size=(50, 10), disabled=True, key="-MESSAGE-")],
        [
            sg.Button("Recibir", key="-START-"),
            sg.Button("Parar", key="-STOP-"),
            sg.Button("Limpiar", key="-CLEAN-"),
            sg.Button("Salir", key="-EXIT1-"),
        ],
    ]

    section2 = [
        [
            sg.Text("Archivo:"),
            sg.In(size=30, enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("Nombre de archivo:"),
            sg.In(default_text="", size=30, key="-FILE_NAME-"),
        ],
        [
            sg.Text(
                "Error: ruta de archivo no válida.",
                text_color="red",
                background_color="black",
                visible=False,
                key="-PATH-ERROR-MSG-",
            ),
        ],
        [
            sg.Button("Guardar", key="-SAVE-"),
            sg.Button("Salir", key="-EXIT2-"),
        ],
    ]

    layout = [
        [sg.Text("Receptor")],
        [
            sg.Radio(
                " Mostrar texto",
                "Radio",
                default=True,
                enable_events=True,
                key="-TOGGLE SEC1-RADIO-",
            ),
            sg.Radio(
                " Guardar en archivo",
                "Radio",
                enable_events=True,
                key="-TOGGLE SEC2-RADIO-",
            ),
        ],
        [
            sg.Column(section1, key="-SEC1-"),
            sg.Column(section2, key="-SEC2-", visible=False),
        ],
    ]

    window = sg.Window("Receptor", layout)
    return window


if __name__ == "__main__":
    main()
