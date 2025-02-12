#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the receiver dummy for the optical communications test
and interact with it.
"""

import os

from paho.mqtt.client import Client as MqttClient
import PySimpleGUI as sg


# Global variable to store the received message
received_message = ""


def main():
    """Main function to start the execution of the receiver program."""

    global received_message

    directory_path = None
    receiving_message = False
    window = define_gui_layout()

    mqtt_client = init_mqtt_client()

    while True:  # Event Loop
        event, values = window.read(timeout=1)
        # print(event, values)
        if event == sg.WIN_CLOSED or event.startswith("-EXIT"):
            break

        # Directory name was filled in, make a list with the files in the provided path
        if event == "-DIR_PATH-":
            directory_path = values["-DIR_PATH-"]

        if event == "-SAVE-":
            if not os.path.isdir(directory_path):
                window["-PATH-ERROR-MSG-"].update(visible=True)

            else:
                window["-PATH-ERROR-MSG-"].update(visible=False)
                file_path = os.path.join(directory_path, values["-FILE_NAME-"])

                # ToDo: Save received message to file
                print(file_path)

        if event == "-RECEIVE-":
            receiving_message = True

        if event == "-STOP-":
            receiving_message = False

        if event == "-CLEAN-":
            received_message = ""
            window["-MESSAGE-"].update(value="")

        if values["-TOGGLE_SEC-SHOW_TEXT-"] and receiving_message:
            window["-MESSAGE-"].update(value=received_message)

        # Show only the selected section, hide the others
        if event.startswith("-TOGGLE_SEC"):
            window["-SEC-SHOW_TEXT-"].update(visible=values["-TOGGLE_SEC-SHOW_TEXT-"])
            window["-SEC-SAVE_FILE-"].update(visible=values["-TOGGLE_SEC-SAVE_FILE-"])

    window.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


def define_gui_layout():
    """Function to define the GUI layout."""

    sec_show_text_visible = True
    sec_save_file_visible = False

    assert (sec_show_text_visible or sec_save_file_visible) == True
    assert (sec_show_text_visible + sec_save_file_visible) == 1

    # ---------------------------------------------------------------------------------

    show_text_section_layout = [
        [sg.Text("Menssage:")],
        [sg.Multiline(size=(50, 10), disabled=True, key="-MESSAGE-")],
        [
            sg.Button("Receive", key="-RECEIVE-"),
            sg.Button("Stop", key="-STOP-"),
            sg.Button("Clean", key="-CLEAN-"),
            sg.Button("Exit", key="-EXIT-1-"),
        ],
    ]

    save_file_section_layout = [
        [
            sg.Text("Directory:"),
            sg.In(size=30, enable_events=True, key="-DIR_NAME-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("File name:"),
            sg.In(default_text="", size=30, key="-FILE_NAME-"),
        ],
        [
            sg.Text(
                "Error: The provided path is not a valid directory.",
                text_color="red",
                background_color="black",
                visible=False,
                key="-PATH-ERROR-MSG-",
            ),
        ],
        [
            sg.Button("Save to file", key="-SAVE-"),
            sg.Button("Exit", key="-EXIT-2-"),
        ],
    ]

    # ---------------------------------------------------------------------------------

    radio_selector_layout = [
        sg.Radio(
            " Show text",
            "Radio",
            default=sec_show_text_visible,
            enable_events=True,
            key="-TOGGLE_SEC-SHOW_TEXT-",
        ),
        sg.Radio(
            " Save to file",
            "Radio",
            default=sec_save_file_visible,
            enable_events=True,
            key="-TOGGLE_SEC-SAVE_FILE-",
        ),
    ]

    sub_sections_layout = [
        sg.Column(
            show_text_section_layout,
            key="-SEC-SHOW_TEXT-",
            visible=sec_show_text_visible,
        ),
        sg.Column(
            save_file_section_layout,
            key="-SEC-SAVE_FILE-",
            visible=sec_save_file_visible,
        ),
    ]

    # ---------------------------------------------------------------------------------

    main_layout = [
        radio_selector_layout,
        sub_sections_layout,
    ]

    window = sg.Window("Receiver", main_layout)
    return window


def init_mqtt_client():
    """Function to initialize the MQTT client."""

    print("Initializing receiver mqtt client...", flush=True)

    mqtt_client = MqttClient("receiver")

    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message

    mqtt_client.connect("mqtt-broker", 1883)
    mqtt_client.loop_start()

    return mqtt_client


def mqtt_on_connect(client, userdata, flags, return_code):
    """Callback function for the MQTT client to handle a connection event."""

    if return_code != 0:
        print(
            f"Failed to connect receiver to mqtt server with error code {return_code}."
        )
        return

    print("Connected receiver to mqtt server.", flush=True)

    client.subscribe("optic-comms-message")

    print("Receiver subscribed to optic-comms-message topic.", flush=True)


def mqtt_on_message(client, userdata, message):
    """Callback function for the MQTT client to handle a message reception event."""

    if message.topic == "optic-comms-message":
        latest_message = message.payload.decode()
        print(f"Received message: {latest_message}", flush=True)

        global received_message
        received_message += latest_message + "\n"


if __name__ == "__main__":
    main()
