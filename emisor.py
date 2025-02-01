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

        if event.startswith("-TOGGLE SEC"):
            # Mostrar/Ocultar secciones
            window["-SEC_PLAIN_TEXT-"].update(
                visible=values["-TOGGLE SEC_PLAIN_TEXT-RADIO-"]
            )
            window["-SEC_FILE-"].update(visible=values["-TOGGLE SEC_FILE-RADIO-"])
            window["-SEC_EXP-"].update(visible=values["-TOGGLE SEC_EXP-RADIO-"])

        if (
            event.startswith("-PARAM-EXP")
            or event == "-TOGGLE SEC_EXP-RADIO-"
            or event == "-SEND-"
        ):
            # Actualizar el ID del experimento
            window["-EXP-ID-"].update(
                value="CO_"
                + f"D{values['-PARAM-EXP-DUMMY_DISTANCE-']}-"
                + f"A{values['-PARAM-EXP-TRANSMITTER_ANGLE-']}-"
                + f"I{values['-PARAM-EXP-LED_INTENSITY-']}-"
                + f"F{values['-PARAM-EXP-BLINKING_FREQUENCY-']}-"
                + f"C{values['-PARAM-EXP-MESSAGES_BATCH-']}-"
                + "Mm"
            )

        if sending_message:
            params = [
                values["-PARAM-EXP-DUMMY_DISTANCE-"],
                values["-PARAM-EXP-TRANSMITTER_ANGLE-"],
                values["-PARAM-EXP-LED_INTENSITY-"],
                values["-PARAM-EXP-BLINKING_FREQUENCY-"],
                values["-PARAM-EXP-MESSAGES_BATCH-"],
            ]

            if values["-TOGGLE SEC_PLAIN_TEXT-RADIO-"]:
                message_data = values["-MESSAGE-"]

            elif values["-TOGGLE SEC_FILE-RADIO-"]:
                file_path = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    message_data = file.read()

            elif values["-TOGGLE SEC_EXP-RADIO-"]:
                # ToDo: implement this part
                message_data = "Experiment message"

            else:
                sys.exit("Error: Something weird happened, transmission type unknown!")

            send_message(message_data, params, mqtt_client)

    window.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


def define_gui_layout():
    """GUI layout"""

    sec_plain_text_visible = True
    sec_exp_visible = False
    sec_file_visible = False

    assert (sec_plain_text_visible or sec_exp_visible or sec_file_visible) == True
    assert (sec_plain_text_visible + sec_exp_visible + sec_file_visible) == 1

    # ---------------------------------------------------------------------------------

    standard_settings_labels = [
        [
            sg.Text("Dummies distance:", expand_x=True),
        ],
        [
            sg.Text("Transmitter angle:", expand_x=True),
        ],
        [
            sg.Text("LEDs intensity:", expand_x=True),
        ],
        [
            sg.Text("Blinking frequency:", expand_x=True),
        ],
    ]

    standard_settings_inputs = [
        [
            sg.In(
                default_text="42",
                size=5,
                enable_events=True,
                key="-PARAM-EXP-DUMMY_DISTANCE-",
            ),
            sg.Text("m"),
        ],
        [
            sg.In(
                default_text="45",
                size=5,
                enable_events=True,
                key="-PARAM-EXP-TRANSMITTER_ANGLE-",
            ),
            sg.Text("º"),
        ],
        [
            sg.In(
                default_text="1",
                size=5,
                enable_events=True,
                key="-PARAM-EXP-LED_INTENSITY-",
            ),
            sg.Text("A"),
        ],
        [
            sg.In(
                default_text="30",
                size=5,
                enable_events=True,
                key="-PARAM-EXP-BLINKING_FREQUENCY-",
            ),
            sg.Text("Hz"),
        ],
    ]

    standard_settings_layout = [
        [
            sg.Column(standard_settings_labels),
            sg.Column(standard_settings_inputs),
        ]
    ]

    # ---------------------------------------------------------------------------------

    experiment_extra_settings_labels = [
        [
            sg.Text("Experiment Id:", expand_x=True),
        ],
        [
            sg.Text("Messages batch:", expand_x=True),
        ],
    ]

    experiment_extra_settings_inputs = [
        [
            sg.Text(text="CO_Dd-Aa-Ii-Ff-Cc-Mm", key="-EXP-ID-"),
        ],
        [
            sg.In(
                default_text="1",
                size=5,
                enable_events=True,
                key="-PARAM-EXP-MESSAGES_BATCH-",
            ),
        ],
    ]

    experiment_extra_settings_layout = [
        [
            sg.Column(experiment_extra_settings_labels),
            sg.Column(experiment_extra_settings_inputs),
        ]
    ]

    # ---------------------------------------------------------------------------------

    plain_text_section_layout = [
        [sg.Text("Message:")],
        [sg.Multiline(size=(50, 10), key="-MESSAGE-")],
    ]

    file_section_layout = [
        [
            sg.Text("File:"),
            sg.In(size=30, enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [sg.Listbox(values=[], enable_events=True, size=(50, 10), key="-FILE LIST-")],
    ]

    experiment_section_layout = experiment_extra_settings_layout

    # ---------------------------------------------------------------------------------

    radio_selector_layout = [
        [
            sg.Radio(
                " Plain text",
                "Radio",
                default=sec_plain_text_visible,
                enable_events=True,
                key="-TOGGLE SEC_PLAIN_TEXT-RADIO-",
            ),
            sg.Radio(
                " File",
                "Radio",
                default=sec_file_visible,
                enable_events=True,
                key="-TOGGLE SEC_FILE-RADIO-",
            ),
            sg.Radio(
                " Experiment",
                "Radio",
                default=sec_exp_visible,
                enable_events=True,
                key="-TOGGLE SEC_EXP-RADIO-",
            ),
        ],
    ]

    sub_sections_layout = [
        [
            sg.Column(
                plain_text_section_layout,
                key="-SEC_PLAIN_TEXT-",
                visible=sec_plain_text_visible,
            ),
            sg.Column(
                file_section_layout,
                key="-SEC_FILE-",
                visible=sec_file_visible,
            ),
            sg.Column(
                experiment_section_layout,
                key="-SEC_EXP-",
                visible=sec_exp_visible,
            ),
        ]
    ]

    common_elements_layout = [
        [
            sg.Column(standard_settings_layout),
        ],
        [
            sg.Button("Send", key="-SEND-"),
            sg.Button("Stop", key="-STOP-"),
            sg.Button("Exit", key="-EXIT-"),
        ],
    ]

    # ---------------------------------------------------------------------------------

    main_layout = [
        radio_selector_layout,
        sub_sections_layout,
        common_elements_layout,
    ]

    window = sg.Window("Transmitter", main_layout)
    return window


def init_mqtt_client():
    """Function to initialize the MQTT client."""

    print("Initializing mqtt client...", flush=True)

    mqtt_client = MqttClient("transmitter")

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
