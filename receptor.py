#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the receiver dummy for the optical communications test
and interact with it.
"""

import os
import sys

from paho.mqtt.client import Client as MqttClient
import PySimpleGUI as sg


# Global variable to store the received message
received_message = ""


def main():
    """Main function to start the execution of the receiver program."""

    global received_message

    folder = None
    receiving_message = False
    window = define_gui_layout()

    mqtt_client = init_mqtt_client()

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
            received_message = ""
            window["-MESSAGE-"].update(value="")

        if values["-TOGGLE SEC1-RADIO-"] and receiving_message:
            window["-MESSAGE-"].update(value=received_message)

        if event.startswith("-TOGGLE SEC"):
            window["-SEC1-"].update(visible=values["-TOGGLE SEC1-RADIO-"])
            window["-SEC2-"].update(visible=values["-TOGGLE SEC2-RADIO-"])

    window.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


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


def init_mqtt_client():
    """Initialize the MQTT client."""

    print("Initializing mqtt client...", flush=True)

    mqtt_client = MqttClient("receptor")

    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message

    mqtt_client.connect("mqtt-broker", 1883)
    mqtt_client.loop_start()

    return mqtt_client


def mqtt_on_connect(client, userdata, flags, return_code):
    """Callback function for the MQTT client to handle a connection event."""

    if return_code != 0:
        print(f"Failed to connect to mqtt server with error code {return_code}.")
        return

    print("Connected to mqtt server.", flush=True)

    client.subscribe("optic-comms-message")

    print("Subscribed to optic-comms-message topic.", flush=True)


def mqtt_on_message(client, userdata, message):
    """Callback function for the MQTT client to handle a message reception event."""

    if message.topic == "optic-comms-message":
        latest_message = message.payload.decode()
        print(f"Received message: {latest_message}", flush=True)

        global received_message
        received_message += latest_message + "\n"


if __name__ == "__main__":
    main()
