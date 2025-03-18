"""
Callback functions to use with the events created by PySimpleGUI

Functions must have two parameters: window (representing the PySimpleGUI's Window Object) and values
"""

import PySimpleGUI as sg
import json
import os

from utils import *
from keys import *

def load_settings_callback(window, values):
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
    
    if values[Keys.TOGGLE_SEQ]:
        load_sequence(settings_file, window)
        return

    try:
        load_settings(settings_file, window)
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
    settings_visibility = not values[Keys.TOGGLE_SEQ]
    window[Keys.STANDARD_SETTINGS].update(visible=settings_visibility)

def send_callback(window, values):
    """
    Callback for the Send event.
    """
    if values[Keys.TOGGLE_PLAIN_TEXT]:
        message_data = values[Keys.MESSAGE]

    elif values[Keys.TOGGLE_FILE]:
        file_path = os.path.join(
            values[Keys.DIR_PATH], values[Keys.FILES_LIST][0]
        )
        with open(file_path, "r", encoding="utf-8-sig") as file:
            message_data = file.read()

    elif values[Keys.TOGGLE_EXP]:
        send_experiment(get_current_settings(window))
        return # Skip sending the message again

    elif values[Keys.TOGGLE_SEQ]:
        failed_files = []
        failed_files_ind = []
        #for file_path in window[Keys.FILES_PATH].get_list_values():
        for [ind, [file_path]] in enumerate(window[Keys.FILES_PATH].Values):
            try:
                load_settings(file_path, window)
                send_experiment(get_current_settings(window))
            except:
                failed_files.append(file_path)
                failed_files_ind.append(ind)
        if len(failed_files) != 0:
            window[Keys.FILES_PATH].update(row_colors=list(zip(failed_files_ind, ["red"] * len(failed_files_ind))))
            sg.popup("Error sending the following experiment(s):\n" + "\n".join(failed_files))

        return # Skip sending the message again

    else:
        # ToDo: Change this to a popup quick message
        sg.popup_quick_message(
            "Error: Something weird happened, transmission type unknown!",
            auto_close_duration=2,
            background_color="yellow",
            text_color="black"
        )

    send_message(message_data, get_current_settings(window))

def add_files(window, values):
    new_files = sg.popup_get_file("Select the file(s): ", multiple_files=True)
    if new_files == None:
        return
    new_files = new_files.split(";") # ; is the default file delimitator
    #current_files = window[Keys.FILES_PATH].get_list_values()
    current_files = window[Keys.FILES_PATH].Values
    #num_current_files = len(current_files)
    #new_files = zip(range(num_current_files, num_current_files + len(new_files)), new_files)
    #new_files = list(new_files)
    new_files = list(map(lambda file: [file], new_files))
    window[Keys.FILES_PATH].update(current_files + new_files)

def remove_files(window, values):
    #files_to_remove = window[Keys.FILES_PATH].get_indexes()
    files_to_remove = window[Keys.FILES_PATH].get()
    #current_files = window[Keys.FILES_PATH].get_list_values()
    current_files = window[Keys.FILES_PATH].Values
    final_files = [file for [ind, file] in enumerate(current_files) if ind not in files_to_remove]
    window[Keys.FILES_PATH].update(final_files)

def move_file_callback_generator(isMoveUp: bool):
    """
    Generates a callback to move the selected files up or down, depending on the given parameter

    Argument `isMoveUp` must be a boolean
    """
    if isMoveUp == True:
        offset = -1
    elif isMoveUp == False:
        offset = 1
    else:
        raise "ERROR: The 'isMoveUp' argument expected a bool value"
    def move_file_callback(window, values):
        #selected_files = window[Keys.FILES_PATH].get_indexes()
        selected_files = window[Keys.FILES_PATH].get()
        if offset > 0:
            iterator = reversed(selected_files)
        else:
            iterator = iter(selected_files)
        #all_files = window[Keys.FILES_PATH].get_list_values()
        all_files = window[Keys.FILES_PATH].Values
        highlight_indexes = []
        for i in iterator:
            ind_to_swap_with = i + offset
            if ind_to_swap_with >= 0 and ind_to_swap_with < len(all_files) and not ind_to_swap_with in highlight_indexes:
                all_files[i], all_files[ind_to_swap_with] = all_files[ind_to_swap_with], all_files[i]
                highlight_indexes.append(ind_to_swap_with)
            else: # Can't move the item
                highlight_indexes.append(i)
        #window[Keys.FILES_PATH].update(all_files, set_to_index=highlight_indexes)
        window[Keys.FILES_PATH].update(all_files, select_rows=highlight_indexes)   

    return move_file_callback