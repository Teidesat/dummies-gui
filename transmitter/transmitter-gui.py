#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the transmitter dummy for the optical communications
test and interact with it.
"""

import json
import os
import sys

import PySimpleGUI as sg
from requests import post as post_request


# Set the debug mode to True to print logs in the console
DEBUG_MODE = True


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

    main_window = define_main_gui_layout()
    update_settings(DEFAULT_SETTINGS, main_window)

    while True:  # Event Loop
        event, values = main_window.read(timeout=1)
        # print(event, values, flush=DEBUG_MODE)
        if event == sg.WIN_CLOSED or event == "-EXIT-":
            break

        if event == "-LOAD_SETTINGS-":
            load_settings(main_window)

        if event == "-SAVE_SETTINGS-":
            # ToDo: Save the settings to a JSON file
            # save_settings(values)
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
            # Update the experiment id based on the currently provided settings
            main_window["-EXP-ID-"].update(
                get_current_experiment_id(get_current_settings(values))
            )

        if event == "-STOP-":
            # ToDo: Send a request to stop the optical communications
            # stop_optical_communications()
            sg.popup_quick_message(
                "Not implemented yet, work in progress.",
                auto_close_duration=2,
                background_color="yellow",
                text_color="black",
            )

        if event == "-SEND-":
            if values["-TOGGLE_SEC-PLAIN_TEXT-"]:
                message_data = values["-MESSAGE-"]

            elif values["-TOGGLE_SEC-FILE-"]:
                file_path = os.path.join(
                    values["-DIR_PATH-"], values["-FILES_LIST-"][0]
                )
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    message_data = file.read()

            elif values["-TOGGLE_SEC-EXP-"]:
                # ToDo: Obtain the experiment messages from the selected messages batch
                #  and adapt the code as needed to handle this case
                # messages_batch = get_messages_batch(values["-PARAM-MESSAGES_BATCH-"])
                message_data = "Experiment message"

            else:
                # ToDo: Change this to a popup quick message
                sys.exit("Error: Something weird happened, transmission type unknown!")

            send_message(message_data, get_current_settings(values))

    main_window.close()


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


def get_current_settings(values):
    """Function to get the current settings based on the provided values."""

    settings = {
        setting_key: float(values[element_key])
        for setting_key, element_key in SETTINGS_KEYS_TO_ELEMENTS_KEYS.items()
    }

    return settings


def get_current_experiment_id(settings):
    """Function to get the current experiment ID based on the provided settings."""

    experiment_id = (
        "CO_"
        + f"D{settings['dummy_distance']}-"
        + f"A{settings['transmitter_angle']}-"
        + f"I{settings['led_intensity']}-"
        + f"F{settings['blinking_frequency']}-"
        + f"L{settings['messages_batch']}-"
        + "Mm"
    )

    return experiment_id


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


def send_message(message_data, settings):
    """Function to send the message to the receiver dummy."""

    experiment_id = get_current_experiment_id(settings)

    print(
        f"Experiment ID: {experiment_id} "
        + f"\n  - Message: {message_data} "
        + f"\n  - Settings: {settings}",
        flush=DEBUG_MODE,
    )

    response = post_request(
        "http://transmitter-server:5000/start_optical_communications",
        headers={"Content-Type": "application/json"},
        json={
            "experiment_id": experiment_id,
            "message": message_data,
            "settings": settings,
        },
    )

    if response.status_code != 200:
        # ToDo: Catch this exception to show a popup message
        raise ConnectionError(
            f"Failed to send message to server with error code {response.status_code}."
        )


if __name__ == "__main__":
    main()
