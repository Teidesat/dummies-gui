#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define callbacks to be used in the main loop.
"""

import datetime
import os
import time

import FreeSimpleGUI as Fsg

from gui_data import GUIData
from keys import Keys
from utils import (
    assert_directory,
    ascii_to_binary,
    binary_to_ascii,
    get_buffer_size,
    get_experiment,
    receive_message,
    save_messages_to_csv,
    update_params,
)


def visibility_callback(window: Fsg.Window, values, data: GUIData):
    """
    Updates the visibility of the elements on the GUI.
    """

    window[Keys.SEC_SHOW_TEXT].update(visible=values[Keys.TOGGLE_SEC_SHOW_TEXT])
    window[Keys.SEC_SAVE_FILE].update(visible=values[Keys.TOGGLE_SEC_SAVE_FILE])
    window[Keys.SEC_EXPERIMENT].update(visible=values[Keys.TOGGLE_SEC_EXPERIMENT])
    window[Keys.SEC_SEQUENCE].update(visible=values[Keys.TOGGLE_SEC_SEQUENCE])


def save_message(window: Fsg.Window, values, data: GUIData):
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

        except:  # ToDo: Catch the exception with the explicit error type
            Fsg.popup_error(
                f"There was an error while saving the message in {file_path}"
            )
            return

        Fsg.popup(f"File {file_path} was correctly saved")


def get_experiment_callback(window: Fsg.Window, values, data: GUIData):
    # ToDo: Add docstring to the function

    save_directory = values[Keys.EXP_SAVE_DIR]

    if not assert_directory(save_directory):
        return

    exp_id, settings, messages = get_experiment()

    window[Keys.EXPERIMENT_ID].update(exp_id)
    update_params(window, settings)
    window[Keys.EXPERIMENT_TABLE].update(messages)

    if len(messages) != 0:
        save_messages_to_csv(messages, save_directory, exp_id)


def _append_messages_to_console(window: Fsg.Window, messages):
    """
    Appends the received messages to the text console in the GUI.
    """

    if len(messages) == 0:
        return

    formatted_lines = []
    for message in messages:
        if isinstance(message, (list, tuple)) and len(message) >= 2:
            formatted_lines.append(f"{message[0]}: {message[1]}")
        else:
            formatted_lines.append(str(message))

    text_to_append = "\n".join(formatted_lines) + "\n"
    window[Keys.MESSAGE].update(text_to_append, append=True)


def _save_in_recording_file(data: GUIData, message) -> None:
    """
    Appends a message to the recording file when recording is enabled.
    """

    if isinstance(message, (list, tuple)) and len(message) >= 2:
        data.append_record(f"{message[0]}: {message[1]}")
        return

    data.append_record(str(message))


def toggle_recording(window: Fsg.Window, values, data: GUIData):
    """
    Starts/stops recording all incoming messages into a text file.
    """

    if data.recording_enabled:
        end_dt = datetime.datetime.now()

        start_ts = getattr(data, "record_start_time", 0.0)
        if start_ts > 0:
            duration_seconds = max(0, int(end_dt.timestamp() - start_ts))
            duration = str(datetime.timedelta(seconds=duration_seconds))
            data.append_record(f"[recording time: {duration}]")
            data.record_start_time = 0.0

        file_path = data.stop_recording()
        window[Keys.RECORD].update("Record")

        if file_path is not None:
            Fsg.popup(f"Recording stopped. File saved in {file_path}")

        return

    save_directory = data.directory_path

    if not save_directory:
        save_directory = values[Keys.SEQ_SAVE_DIR]

    if not assert_directory(save_directory):
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(save_directory, f"receiver_record_{timestamp}.txt")

    try:
        data.start_recording(file_path)

    except OSError:
        Fsg.popup_error(f"Error opening recording file: {file_path}")
        return

    data.record_start_time = time.time()

    window[Keys.RECORD].update("Stop")
    Fsg.popup(f"Recording started in {file_path}")


def receive_sequence(window: Fsg.Window, values, data: GUIData):
    """
    Receives a sequence of messages and updates the table
    """

    data.receiving_message = True

    save_directory = values[Keys.SEQ_SAVE_DIR]
    if not assert_directory(save_directory):
        return

    exp_size = get_buffer_size()
    if exp_size == 0:
        Fsg.popup("There is no experiment ready")
        return

    # Get current table values
    existing_data = window[Keys.SEQUENCES_TABLE].Values
    if existing_data is None:
        existing_data = []

    new_data = []
    for _ in range(int(exp_size)):
        exp_id, _, messages = get_experiment()

        if len(messages) != 0:
            for message in messages:
                new_data.append(message)
                _save_in_recording_file(data, message)

            _append_messages_to_console(window, messages)

            exp_id = exp_id + "_" + str(datetime.datetime.now().isoformat())
            save_messages_to_csv(messages, save_directory, exp_id)

    window[Keys.SEQUENCES_TABLE].update(existing_data + new_data)


def receive(window: Fsg.Window, values, data: GUIData):
    """
    Receives a single message
    """

    try:
        data.message = receive_message()

        if not values[Keys.USE_BINARY]:
            data.message = binary_to_ascii(data.message)

    except:  # ToDo: Catch the exception with the explicit error type
        data.message = "Error receiving message"

    _save_in_recording_file(data, data.message)

    window[Keys.MESSAGE].update(value=data.message)


def transform_binary_ascii(window: Fsg.Window, values, data: GUIData):
    """
    Transforms the text in the text section into binary or ASCII
    """

    if values[Keys.USE_BINARY]:
        data.message = ascii_to_binary(values[Keys.MESSAGE])

    else:
        data.message = binary_to_ascii(values[Keys.MESSAGE])

    window[Keys.MESSAGE].update(data.message)
