#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the transmitter dummy for the optical communications
test and interact with it.
"""

import os
import sys

from paho.mqtt.client import Client as MqttClient
import PySimpleGUI as sg


def main():
    """Main function to start the execution of the transmitter program."""

    sending_message = False
    window = define_gui_layout()

    mqtt_client = init_mqtt_client()

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
                # values["-PARAM-EXP-ID-"],
                # values["-PARAM-EXP-SENDER_ANGLE-"],
                # values["-PARAM-EXP-LED_POWER-"],
                # values["-PARAM-EXP-BLINKING_FREQUENCY-"],
                # values["-PARAM-EXP-DUMMY_DISTANCE-"],
                values["-PARAM-FREQUENCY-"],
                values["-PARAM-DUTY_CYCLE-"],
            ]

            if values["-TOGGLE SEC_PTEXT-RADIO-"]:
                message_data = values["-MESSAGE-"]

            elif values["-TOGGLE SEC_FILE-RADIO-"]:
                file_path = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    message_data = file.read()

            else:
                sys.exit("Error: Algo raro ha pasado, tipo de emisión desconocida!")

            send_message(message_data, params, mqtt_client)

        if event.startswith("-TOGGLE SEC"):
            # is_experiment = (
            #     values["-TOGGLE SEC_EXP-RADIO-"]
            # )
            # window["-IL-PTEXT_FOLDER-"].update(visible=not is_exp)
            # window["-IL-PTEXT_FOLDER-"].update(visible=is_exp)

            # Mostrar/Ocultar secciones
            window["-SEC_PTEXT-"].update(visible=values["-TOGGLE SEC_PTEXT-RADIO-"])
            window["-SEC_FILE-"].update(visible=values["-TOGGLE SEC_FILE-RADIO-"])
            window["-IL-EXP-"].update(visible=values["-TOGGLE SEC_EXP-RADIO-"])
            window["-IL-PTEXT_FOLDER-"].update(visible=not values["-TOGGLE SEC_EXP-RADIO-"])

    window.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


def define_gui_layout():
    """GUI layout"""

    buttons = [
        [
            sg.Button("Enviar", key="-SEND-"),
            sg.Button("Parar", key="-STOP-"),
            sg.Button("Salir", key="-EXIT-"),
        ]
    ]

    labels = [
        [
            sg.Text("Frecuencia:"),
        ],
        [
            sg.Text("Duty cycle:"),
        ],
    ]

    inputs = [
        [
            sg.In(default_text="30", size=5, key="-PARAM-FREQUENCY-"),
            sg.Text("KHz"),
        ],
        [
            sg.In(default_text="65", size=5, key="-PARAM-DUTY_CYCLE-"),
            sg.Text("%"),
        ],
    ]

    labelInputFieldsLayout = [
        [
            sg.Column(labels),
            sg.Column(inputs),
        ]
    ]

    inputLayoutPTextFile = sg.Column(
        [
            [
                sg.Column(labelInputFieldsLayout),
                sg.Column(buttons),
            ]
        ],
        key="-IL-PTEXT_FOLDER-",
        visible=True,
    )

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

    # ---------------------------- Experiment part ----------------------------
    inputsExperiment = [
        [
            sg.In(default_text="12345678", size=10, key="-PARAM-EXP-ID-"),
        ],
        [
            sg.In(default_text="45", size=5, key="-PARAM-EXP-SENDER_ANGLE-"),
            sg.Text("º"),
        ],
        [
            sg.In(default_text="1", size=5, key="-PARAM-EXP-LED_POWER-"),
            sg.Text("A"),
        ],
        [
            sg.In(default_text="30", size=5, key="-PARAM-EXP-BLINKING_FREQUENCY-"),
            sg.Text("kbps"),
        ],
        [
            sg.In(default_text="42", size=5, key="-PARAM-EXP-DUMMY_DISTANCE-"),
            sg.Text("<unit>"),
        ],
    ]

    labelsExperiment = [
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

    inputLayoutExperiment = sg.Column(
        [
            [
                sg.Column(labelsExperiment),
                sg.Column(inputsExperiment),
            ],
            [
                sg.Button("Execute experiment", key="-EXEC-",expand_x=True),
            ]
        ],
        key="-IL-EXP-",
        visible=False,
        expand_x=True
    )
    # -------------------------------------------------------------------------

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
            # Sections
            sg.Column(sectionPText, key="-SEC_PTEXT-"),
            sg.Column(sectionFile, key="-SEC_FILE-", visible=False),
            inputLayoutExperiment,
        ],
        [
            # Input layout
            inputLayoutPTextFile,
        ],
    ]

    window = sg.Window("Emisor", layout)
    return window


def init_mqtt_client():
    """Function to initialize the MQTT client."""

    print("Initializing mqtt client...", flush=True)

    mqtt_client = MqttClient("emisor")

    mqtt_client.on_connect = mqtt_on_connect

    mqtt_client.connect("mqtt-broker", 1883)
    mqtt_client.loop_start()

    return mqtt_client


def mqtt_on_connect(client, userdata, flags, return_code):
    """Callback function for the MQTT client to handle a connection event."""

    if return_code != 0:
        print(f"Failed to connect to mqtt server with error code {return_code}.")
        return

    print("Connected to mqtt server.", flush=True)


def send_message(message_data, params, mqtt_client):
    """Function to send the message to the receiver dummy."""

    # ToDo: Enviar el mensaje y los parámetros al codificador de mensajes en pulsos de luz
    print(f"Message: {message_data} - Parameters: {params}")

    mqtt_client.publish(
        "optic-comms-message",
        message_data,
    )


if __name__ == "__main__":
    main()
