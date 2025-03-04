"""
Callback functions to use with the events created by PySimpleGUI

Functions must have two parameters: window (representing the PySimpleGUI's Window Object) and values
"""

import PySimpleGUI as sg
import json
import os

from utils import *
from keys import *

def load_settings(window, values):
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

def update_visibility(window, values):
    window[Keys.SEC_PLAIN_TEXT.value].update(visible=values[Keys.TOGGLE_PLAIN_TEXT.value])
    window[Keys.SEC_FILE.value].update(visible=values[Keys.TOGGLE_FILE.value])
    window[Keys.SEC_EXP.value].update(visible=values[Keys.TOGGLE_EXP.value])
    window[Keys.SEC_SEQ.value].update(visible=values[Keys.TOGGLE_SEQ.value])

def send_callback(window, values):
    if values[Keys.TOGGLE_PLAIN_TEXT.value]:
        message_data = values[Keys.MESSAGE.value]

    elif values[Keys.TOGGLE_FILE.value]:
        file_path = os.path.join(
            values[Keys.DIR_PATH.value], values[Keys.FILES_LIST.value][0]
        )
        with open(file_path, "r", encoding="utf-8-sig") as file:
            message_data = file.read()

    elif values[Keys.TOGGLE_EXP.value]:
        # ToDo: Obtain the experiment messages from the selected messages batch
        #  and adapt the code as needed to handle this case
        # messages_batch = get_messages_batch(values["-PARAM-MESSAGES_BATCH-"])
        send_experiment(get_current_settings(values))
        pass

    elif values[Keys.TOGGLE_SEQ.value]:
        for file_path in values[Keys.FILES_LIST.value]:
            send_experiment()
        return # Skip sending the message again

    else:
        # ToDo: Change this to a popup quick message
        sg.sg.popup_quick_message(
            "Error: Something weird happened, transmission type unknown!",
            auto_close_duration=2,
            background_color="yellow",
            text_color="black"
        )

    send_message(message_data, get_current_settings(values))