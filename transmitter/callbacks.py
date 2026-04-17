#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Callback functions to use with the events created by PySimpleGUI.

Functions must have two parameters: window (representing the FreeSimpleGUI's Window
Object) and values.
"""

import json
import os

from dotenv import load_dotenv
import FreeSimpleGUI as Fsg

from progress_popup.progress_popup import run_progress_window

from keys import Keys
load_dotenv()
BASE_URL = os.getenv("TRANSMITTER_SERVER_BASE_URL")
from utils import (
    load_sequence,
    load_settings,
    get_current_settings,
    str_to_binary_str,
    send_experiment,
    send_message,
)



def load_settings_callback(window: Fsg.Window, values) -> None:
    """
    Function to load the settings from the selected file.

    Note: This function modifies the window object in place as an intended side effect.
    """

    settings_file = Fsg.popup_get_file(
        "Select the file with the settings to be loaded",
        file_types=(
            ("JSON files", ".json"),
            ("ALL Files", ". *"),
        ),
        no_window=True,
    )

    if settings_file is None:
        Fsg.popup("File selection canceled, no settings were loaded.")
        return

    if values[Keys.TOGGLE_SEQ]:  # If the program is in sequence mode
        load_sequence(settings_file, window)
        return

    try:
        load_settings(settings_file, window)

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        KeyError,
    ):
        Fsg.popup("Error loading settings from file, please try again.")


def update_visibility(window: Fsg.Window, values) -> None:
    """
    Updates the visibility of the elements on the GUI.
    """

    window[Keys.SEC_PLAIN_TEXT].update(visible=values[Keys.TOGGLE_PLAIN_TEXT])
    window[Keys.SEC_FILE].update(visible=values[Keys.TOGGLE_FILE])
    window[Keys.SEC_EXP].update(visible=values[Keys.TOGGLE_EXP])
    window[Keys.SEC_SEQ].update(visible=values[Keys.TOGGLE_SEQ])
    window[Keys.STANDARD_SETTINGS].update(visible=(not values[Keys.TOGGLE_SEQ]))


def send_callback(window: Fsg.Window, values) -> None:
    """
    Callback for the 'Send' event.
    """

    if values[Keys.TOGGLE_PLAIN_TEXT]:
        message_data = values[Keys.MESSAGE]

        if not message_data or message_data.strip() == "":
            Fsg.popup_quick_message(
                "Please enter a message to send",
                auto_close_duration=2,
                background_color="yellow",
                text_color="black",
            )
            return


    elif values[Keys.TOGGLE_FILE]:
        if not values[Keys.FILES_LIST] or len(values[Keys.FILES_LIST]) == 0:
            Fsg.popup_quick_message(
                "Please select a file first",
                auto_close_duration=2,
                background_color="yellow",
                text_color="black",
            )
            return
        file_path = os.path.join(values[Keys.DIR_PATH], values[Keys.FILES_LIST][0])
        with open(file_path, "r", encoding="utf-8-sig") as file:
            message_data = file.read()           


    elif values[Keys.TOGGLE_EXP]:
        try:
            if not send_experiment(get_current_settings(window)):
                return
        # send_experiment(get_current_settings(window))
            run_progress_window()
        except Exception as e:
            Fsg.popup_error(f"Error launching experiment: {str(e)}")
        return  # Skip sending the message again

    elif values[Keys.TOGGLE_SEQ]:
        failed_files = []
        failed_files_ind = []

        # 1. Obtenemos los ajustes actuales de la interfaz (velocidad, ángulo, etc.)
        current_settings = get_current_settings(window)

        for [ind, [file_path]] in enumerate(window[Keys.FILES_PATH].Values):
            try:
                # 2. Truco para que el "experiment_id" sea correcto: 
                # Extraemos el número del archivo (ej. de "batch-1.csv" sacamos el "1")
                filename = os.path.basename(file_path)
                if "batch-" in filename:
                    batch_num = filename.split("batch-")[1].split(".")[0]
                    current_settings["messages_batch"] = float(batch_num)

                # 3. Leemos el archivo CSV directamente y enviamos cada línea
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    for line in file:
                        line_clean = line.strip()
                        if not line_clean: 
                            continue # Saltamos líneas vacías por seguridad
                        
                        [message_id, message] = line_clean.split(",")
                        
                        # Si está marcado el tick de "Encode to binary", lo convertimos
                        if values[Keys.ENCODE_MESSAGE]:
                            message = str_to_binary_str(message)
                            
                        # Lo mandamos directo al servidor
                        send_message(message, current_settings, message_id)

            except Exception as e:
                print(f"Error procesando {file_path}: {e}") # Por si queremos depurar
                failed_files.append(file_path)
                failed_files_ind.append(ind)

        run_progress_window()

        if len(failed_files) != 0:
            window[Keys.FILES_PATH].update(
                row_colors=list(
                    zip(
                        failed_files_ind,
                        ["red"] * len(failed_files_ind),
                    )
                )
            )
            Fsg.popup(
                "Error sending the following experiment(s):\n"
                + "\n".join(failed_files),
            )

        return  # Skip sending the message again



    else:
        Fsg.popup_quick_message(
            "Error: Something weird happened, transmission type unknown!",
            auto_close_duration=2,
            background_color="yellow",
            text_color="black",
        )
        return

    # Check if the user wants to encode the message to binary
    if values[Keys.ENCODE_MESSAGE]:
        message_data = str_to_binary_str(message_data)
    send_message(message_data, get_current_settings(window))

    #run_progress_window()  #this is a test only for the issue #25
    Fsg.popup_quick_message(
        "Message sent successfully!",
        auto_close_duration=2,
        background_color="green",
        text_color="white",
    )


def add_files(window: Fsg.Window, values) -> None:
    # ToDo: Add docstring to the function

    new_files = Fsg.popup_get_file(
        "Select the file(s): ",
        file_types=(
            ("CSV files", ".csv"),
            ("ALL Files", ". *"),
        ),
        multiple_files=True,
        no_window=True,
    )

    if new_files is None:
        Fsg.popup("File selection canceled, no new files were loaded.")
        return

    # ToDo: For each file, check if its a valid experiment file

    current_files = window[Keys.FILES_PATH].Values
    new_files = list(map(lambda file: [file], new_files))

    window[Keys.FILES_PATH].update(current_files + new_files)


def remove_files(window: Fsg.Window, values) -> None:
    # ToDo: Add docstring to the function

    files_indexes_to_remove = window[Keys.FILES_PATH].get()
    current_files_paths = window[Keys.FILES_PATH].Values

    final_files_paths = [
        file_path
        for [file_index, file_path] in enumerate(current_files_paths)
        if file_index not in files_indexes_to_remove
    ]

    window[Keys.FILES_PATH].update(final_files_paths)

def stop_callback(window: Fsg.Window, values) -> None:
    """
    Callback for the 'Stop' event.
    """
    from progress_popup.callbacks import stop_communication

    try:
        stop_communication()
        Fsg.popup_quick_message(
            "Communication stopped successfully.",
            auto_close_duration=2,
            background_color="green",
            text_color="white",
        )
    except Exception as e:
        Fsg.popup_quick_message(
            f"Error stopping communication: {str(e)}",
            auto_close_duration=2,
            background_color="red",
            text_color="white",
        )

def move_file_callback_generator(is_move_up: bool) -> callable:
    """
    Generates a callback to move the selected files up or down, depending on the given parameter

    Argument `is_move_up` must be a boolean
    """

    if is_move_up:
        offset = -1
    elif not is_move_up:
        offset = 1
    else:
        raise ValueError("The 'is_move_up' argument expected a bool value")

    def move_file_callback(window, values):
        # ToDo: Add docstring to the function

        selected_files = window[Keys.FILES_PATH].get()

        if offset > 0:
            iterator = reversed(selected_files)
        else:
            iterator = iter(selected_files)

        all_files = window[Keys.FILES_PATH].Values
        highlight_indexes = []

        for i in iterator:
            ind_to_swap_with = i + offset

            if (
                0 <= ind_to_swap_with < len(all_files)
                and ind_to_swap_with not in highlight_indexes
            ):
                all_files[i], all_files[ind_to_swap_with] = (
                    all_files[ind_to_swap_with],
                    all_files[i],
                )
                highlight_indexes.append(ind_to_swap_with)

            else:  # Can't move the item
                highlight_indexes.append(i)

        # window[Keys.FILES_PATH].update(all_files, set_to_index=highlight_indexes)
        window[Keys.FILES_PATH].update(all_files, select_rows=highlight_indexes)

    return move_file_callback
