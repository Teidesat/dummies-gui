"""
Define callbacks to be used in the main loop
"""

import os
import json
import csv
import FreeSimpleGUI as sg
import datetime

from utils import *
from keys import *
from utils import *
from gui_data import GUIData


def visibility_callback(window, values, data: GUIData):
    """
    Updates the visibility of the elements on the GUI
    """
    window[Keys.SEC_SHOW_TEXT].update(visible=values[Keys.TOGGLE_SEC_SHOW_TEXT])
    window[Keys.SEC_SAVE_FILE].update(visible=values[Keys.TOGGLE_SEC_SAVE_FILE])
    window[Keys.SEC_EXPERIMENT].update(visible=values[Keys.TOGGLE_SEC_EXPERIMENT])
    window[Keys.SEC_SEQUENCE].update(visible=values[Keys.TOGGLE_SEC_SEQUENCE])


def save_message(window, values, data: GUIData):
    """
    Saves the message in the selected file path
    """

    directory_path = data.directory_path
    if not os.path.isdir(directory_path):
        window[Keys.PATH_ERROR_MSG].update(visible=True)

    else:
        window[Keys.PATH_ERROR_MSG].update(visible=False)
        file_path = os.path.join(directory_path, values[Keys.FILE_NAME])
        try:
            with open(file_path, "w") as file:
                message = receive_message()
                file.write(message)
        except:
            sg.popup_error(
                f"There was an error while saving the message in {file_path}"
            )
            return
        sg.popup(f"File {file_path} was correctly saved")


def get_experiment_callback(window: sg.Window, values, data: GUIData):
    save_directory = values[Keys.EXP_SAVE_DIR]
    if not assert_directory(save_directory):
        return
    id, settings, messages = get_experiment()
    window[Keys.EXPERIMENT_ID].update(id)
    update_params(window, settings)
    # messages = get_messages(id)
    window[Keys.EXPERIMENT_TABLE].update(messages)
    if len(messages) != 0:
        save_messages_to_csv(messages, save_directory, id)


def receive_sequence(window, values, data: GUIData):
    """
    Receives a sequence of messages and updates the table
    """
    data.receiving_message = True
    save_directory = values[Keys.SEQ_SAVE_DIR]
    if not assert_directory(save_directory):
        return
    exp_size = get_buffer_size()
    if exp_size == 0:
        sg.popup("There is no experiment ready")
        return
    existing_data = window[Keys.SEQUENCES_TABLE].Values  # Get current table values
    if existing_data is None:
        existing_data = []
    new_data = []
    for i in range(int(exp_size)):
        id, settings, messages = get_experiment()
        if len(messages) != 0:
            for message in messages:
                new_data.append(message)
            id = id + "_" + str(datetime.datetime.now().isoformat())
            save_messages_to_csv(messages, save_directory, id)
    window[Keys.SEQUENCES_TABLE].update(existing_data + new_data)


def receive(window, values, data: GUIData):
    """
    Receives a single message
    """

    try:
        data.message = receive_message()
        if not values[Keys.USE_BINARY]:
            data.message = binary_to_ascii(data.message)
    except:
        data.message = "Error receiving message"
    window[Keys.MESSAGE].update(value=data.message)


def transform_binary_ascii(window: sg.Window, values, data: GUIData):
    """
    Transforms the text in the text section into binary or ASCII
    """
    if values[Keys.USE_BINARY]:
        data.message = ascii_to_binary(values[Keys.MESSAGE])
    else:
        data.message = binary_to_ascii(values[Keys.MESSAGE])
    window[Keys.MESSAGE].update(data.message)
