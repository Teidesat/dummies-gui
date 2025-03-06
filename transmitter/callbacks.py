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
    window[Keys.SEC_PLAIN_TEXT].update(visible=values[Keys.TOGGLE_PLAIN_TEXT])
    window[Keys.SEC_FILE].update(visible=values[Keys.TOGGLE_FILE])
    window[Keys.SEC_EXP].update(visible=values[Keys.TOGGLE_EXP])
    window[Keys.SEC_SEQ].update(visible=values[Keys.TOGGLE_SEQ])

def send_callback(window, values):
    if values[Keys.TOGGLE_PLAIN_TEXT]:
        message_data = values[Keys.MESSAGE]

    elif values[Keys.TOGGLE_FILE]:
        file_path = os.path.join(
            values[Keys.DIR_PATH], values[Keys.FILES_LIST][0]
        )
        with open(file_path, "r", encoding="utf-8-sig") as file:
            message_data = file.read()

    elif values[Keys.TOGGLE_EXP]:
        # ToDo: Obtain the experiment messages from the selected messages batch
        #  and adapt the code as needed to handle this case
        # messages_batch = get_messages_batch(values["-PARAM-MESSAGES_BATCH-"])
        send_experiment(get_current_settings(values))
        pass

    elif values[Keys.TOGGLE_SEQ]:
        for file_path in window[Keys.FILES_PATH].get_list_values():
            # TODO: Need to update the settings for each file of the experiment
            send_experiment(get_current_settings(values))
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

def add_files(window, values):
    new_files = sg.popup_get_file("Select the file(s): ", multiple_files=True)
    if new_files == None:
        return
    new_files = new_files.split(";") # ; is the default file delimitator
    current_files = window[Keys.FILES_PATH].get_list_values()
    new_files = [file for file in new_files if file not in current_files]
    window[Keys.FILES_PATH].update(current_files + new_files)

def remove_files(window, values):
    files_to_remove = values[Keys.FILES_PATH]
    current_files = window[Keys.FILES_PATH].get_list_values()
    final_files = [file for file in current_files if file not in files_to_remove]
    window[Keys.FILES_PATH].update(final_files)