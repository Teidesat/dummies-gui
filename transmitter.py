#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the transmitter dummy for the optical communications
test and interact with it.
"""

import json
import os
import sys

from paho.mqtt.client import Client as MqttClient
import PySimpleGUI as sg


DEFAULT_SETTINGS = {
    "dummy_distance": 3,
    "transmitter_angle": 0,
    "led_intensity": 0.5,
    "blinking_frequency": 30,
    "messages_batch": 1,
}
SETTINGS_KEYS_TO_ELEMENTS_KEYS = {
    "dummy_distance": "-PARAM-DUMMY_DISTANCE-",
    "transmitter_angle": "-PARAM-TRANSMITTER_ANGLE-",
    "led_intensity": "-PARAM-LED_INTENSITY-",
    "blinking_frequency": "-PARAM-BLINKING_FREQUENCY-",
    "messages_batch": "-PARAM-MESSAGES_BATCH-",
}


def main():
    """Main function to start the execution of the transmitter program."""

    sending_message = False
    main_window = define_main_gui_layout()
    update_settings(DEFAULT_SETTINGS, main_window)

    mqtt_client = init_mqtt_client()

    while True:  # Event Loop
        event, values = main_window.read(timeout=1)
        # print(event, values)
        if event == sg.WIN_CLOSED or event == "-EXIT-":
            break

        if event == "-LOAD_SETTINGS-":
            load_settings(main_window)

        if event == "-SAVE_SETTINGS-":
            # ToDo: Implement this part
            sg.popup_quick_message(
                "Not implemented yet, work in progress.",
                auto_close_duration=2,
                background_color="yellow",
                text_color="black",
            )

        # Directory name was filled in, make a list with the files in the provided path
        if event == "-DIR_PATH-":
            main_window["-FILES_LIST-"].update(
                get_files_from_path(values["-DIR_PATH-"])
            )

        if event == "-SEND-":
            sending_message = True

        if event == "-STOP-":
            sending_message = False

        # Show only the selected section, hide the others
        if event.startswith("-TOGGLE_SEC"):
            main_window["-SEC-PLAIN_TEXT-"].update(
                visible=values["-TOGGLE_SEC-PLAIN_TEXT-"]
            )
            main_window["-SEC-FILE-"].update(visible=values["-TOGGLE_SEC-FILE-"])
            main_window["-SEC-EXP-"].update(visible=values["-TOGGLE_SEC-EXP-"])

        if (
            event.startswith("-PARAM")
            or event.endswith("SETTINGS-")
            or event == "-TOGGLE_SEC-EXP-"
            or event == "-SEND-"
        ):
            # Update the experiment id based on the provided parameters
            main_window["-EXP-ID-"].update(
                value="CO_"
                + f"D{values['-PARAM-DUMMY_DISTANCE-']}-"
                + f"A{values['-PARAM-TRANSMITTER_ANGLE-']}-"
                + f"I{values['-PARAM-LED_INTENSITY-']}-"
                + f"F{values['-PARAM-BLINKING_FREQUENCY-']}-"
                + f"C{values['-PARAM-MESSAGES_BATCH-']}-"
                + "Mm"
            )

        if sending_message:
            params = [
                values["-PARAM-DUMMY_DISTANCE-"],
                values["-PARAM-TRANSMITTER_ANGLE-"],
                values["-PARAM-LED_INTENSITY-"],
                values["-PARAM-BLINKING_FREQUENCY-"],
                values["-PARAM-MESSAGES_BATCH-"],
            ]

            if values["-TOGGLE_SEC-PLAIN_TEXT-"]:
                message_data = values["-MESSAGE-"]

            elif values["-TOGGLE_SEC-FILE-"]:
                file_path = os.path.join(
                    values["-DIR_PATH-"], values["-FILES_LIST-"][0]
                )
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    message_data = file.read()

            elif values["-TOGGLE_SEC-EXP-"]:
                # ToDo: implement this part
                message_data = "Experiment message"

            else:
                sys.exit("Error: Something weird happened, transmission type unknown!")

            send_message(message_data, params, mqtt_client)

    main_window.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


def define_main_gui_layout():
    """Function to define the GUI layout of the main window."""

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
                size=5,
                enable_events=True,
                key="-PARAM-DUMMY_DISTANCE-",
            ),
            sg.Text("m"),
        ],
        [
            sg.In(
                size=5,
                enable_events=True,
                key="-PARAM-TRANSMITTER_ANGLE-",
            ),
            sg.Text("º"),
        ],
        [
            sg.In(
                size=5,
                enable_events=True,
                key="-PARAM-LED_INTENSITY-",
            ),
            sg.Text("A"),
        ],
        [
            sg.In(
                size=5,
                enable_events=True,
                key="-PARAM-BLINKING_FREQUENCY-",
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
                size=5,
                enable_events=True,
                key="-PARAM-MESSAGES_BATCH-",
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
            sg.In(size=30, enable_events=True, key="-DIR_PATH-"),
            sg.FolderBrowse(),
        ],
        [sg.Listbox(values=[], enable_events=True, size=(50, 10), key="-FILES_LIST-")],
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
                key="-TOGGLE_SEC-PLAIN_TEXT-",
            ),
            sg.Radio(
                " File",
                "Radio",
                default=sec_file_visible,
                enable_events=True,
                key="-TOGGLE_SEC-FILE-",
            ),
            sg.Radio(
                " Experiment",
                "Radio",
                default=sec_exp_visible,
                enable_events=True,
                key="-TOGGLE_SEC-EXP-",
            ),
        ],
    ]

    sub_sections_layout = [
        [
            sg.Column(
                plain_text_section_layout,
                key="-SEC-PLAIN_TEXT-",
                visible=sec_plain_text_visible,
            ),
            sg.Column(
                file_section_layout,
                key="-SEC-FILE-",
                visible=sec_file_visible,
            ),
            sg.Column(
                experiment_section_layout,
                key="-SEC-EXP-",
                visible=sec_exp_visible,
            ),
        ]
    ]

    common_elements_layout = [
        [
            sg.Column(standard_settings_layout),
        ],
        [
            sg.Button("Load settings", key="-LOAD_SETTINGS-"),
            sg.Button("Save settings", key="-SAVE_SETTINGS-"),
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

    main_window = sg.Window("Transmitter", main_layout, finalize=True)
    return main_window


def load_settings(window):
    """
    Function to load the settings from the selected file.

    Note: This function modifies the window object in place as an intended side effect.
    """

    settings_file = sg.popup_get_file(
        "Select the file with the settings to be loaded",
        file_types=(
            ("JSON files", ".json"),
            ("ALL Files", ". *"),
        ),
        no_window=True,
    )

    if settings_file is None:
        sg.popup("File selection canceled, no settings were loaded.")
        return

    try:
        with open(settings_file, "r") as file:
            settings = json.load(file)

        update_settings(settings, window)

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        KeyError,
    ):
        sg.popup("Error loading settings from file, please try again.")


def update_settings(settings, window):
    """
    Function to update the GUI elements with the provided settings.

    Note: This function modifies the window object in place as an intended side effect.
    """

    for setting_key, element_key in SETTINGS_KEYS_TO_ELEMENTS_KEYS.items():
        window[element_key].update(value=settings[setting_key])


def init_mqtt_client():
    """Function to initialize the MQTT client."""

    print("Initializing transmitter mqtt client...", flush=True)

    mqtt_client = MqttClient("transmitter")

    mqtt_client.on_connect = mqtt_on_connect

    mqtt_client.connect("mqtt-broker", 1883)
    mqtt_client.loop_start()

    return mqtt_client


def mqtt_on_connect(client, userdata, flags, return_code):
    """Callback function for the MQTT client to handle a connection event."""

    if return_code != 0:
        print(
            f"Failed to connect transmitter to mqtt server with error code {return_code}."
        )
        return

    print("Connected transmitter to mqtt server.", flush=True)


def get_files_from_path(target_path):
    """Function to get a list of files from the provided path."""

    try:
        file_list = os.listdir(target_path)
    except FileNotFoundError:
        file_list = []

    return [
        file_name
        for file_name in file_list
        if os.path.isfile(os.path.join(target_path, file_name))
    ]


def send_message(message_data, params, mqtt_client):
    """Function to send the message to the receiver dummy."""

    # ToDo: Send the message and the parameters to the light pulses' message encoder
    print(f"Message: {message_data} - Parameters: {params}")

    mqtt_client.publish(
        "optic-comms-message",
        message_data,
    )


if __name__ == "__main__":
    main()
