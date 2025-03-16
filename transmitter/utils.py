"""
Various utility functions 
"""

import PySimpleGUI as sg
import json
import os
from requests import post as post_request

from keys import *

# Set the debug mode to True to print logs in the console
DEBUG_MODE = True

SETTINGS_KEYS_TO_ELEMENTS_KEYS = {
    "dummy_distance": Keys.PARAM_DUMMY_DISTANCE,
    "transmitter_angle": Keys.PARAM_TRANSMITTER_ANGLE,
    "led_intensity": Keys.PARAM_LED_INTENSITY,
    "blinking_frequency": Keys.PARAM_BLINKING_FREQUENCY,
    "messages_batch": Keys.PARAM_MESSAGES_BATCH,
}


def update_settings(settings, window):
    """
    Function to update the GUI elements with the provided settings.

    Note: This function modifies the window object in place as an intended side effect.
    """

    for setting_key, element_key in SETTINGS_KEYS_TO_ELEMENTS_KEYS.items():
        window[element_key].update(value=settings[setting_key])


def get_current_settings(window):
    """Function to get the current settings based on the provided window."""

    settings = {
        setting_key: float(window[element_key].get() if window[element_key].get() != "" else 0) # Gets the focused element
        for setting_key, element_key in SETTINGS_KEYS_TO_ELEMENTS_KEYS.items()
    }

    return settings


def get_current_experiment_id(settings, id = None):
    """Function to get the current experiment ID based on the provided settings."""
    if id == None:
        id = "m"
    experiment_id = (
        "CO_"
        + f"D{settings['dummy_distance']}-"
        + f"A{settings['transmitter_angle']}-"
        + f"I{settings['led_intensity']}-"
        + f"F{settings['blinking_frequency']}-"
        + f"L{settings['messages_batch']}-"
        + f"M{id}"
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


def send_message(message_data, settings, id):
    """Function to send the message to the receiver dummy."""

    experiment_id = get_current_experiment_id(settings, id)

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

def save_settings(window, path):
    """Save the settings in a given file"""
    if path == None or path == "":
        return
    try:
        file = open(path, "w")
    except:
        sg.popup_error("File could not be opened")
        return
    json.dump(get_current_settings(window), file, indent=2)
    return

def send_experiment(settings):
    message_batch = int(settings["messages_batch"]) # Asserting is just an integer
    message_batch_file_name = os.getcwd() + "/message-batches/batch-" + str(message_batch) + ".csv"
    try:
        with open(message_batch_file_name, "r") as file:
            for line in file:
                line = line.strip()
                [id, messsage] = line.split(",")
                send_message(line, settings, id)
    except:
        sg.popup_error("Experiment file \"" + message_batch_file_name + "\" could not be found")

def retrieve_combo_values(experimentParam):
    """Retrieves the combo box values of a given experiment parameter from its corresponding file. 
       
       Adds .txt at the end of the given parameter."""
    file = open("combobox-values/" + experimentParam + ".txt", "r")
    values = file.read()
    file.close()
    return values.split()

def load_settings(path, window):
    """
    Load settings from the given path.

    This function may throw if there is an error opening the file
    """
    with open(path, "r") as file:
        settings = json.load(file)

    update_settings(settings, window)

def save_sequence(window, path: str):
    """
    Saves the current experiment sequence in the specified path
    """
    savedSequence = ""
    for [expPath] in window[Keys.FILES_PATH].Values:
        savedSequence += expPath + "\n"
    savedSequence = savedSequence.strip()
    try:
        with open(path, "w") as file:
            file.write(savedSequence)
    except:
        sg.popup_error("There was an error while saving the sequence")
    
def load_sequence(path: str, window):
    try: 
        new_sequence = []
        with open(path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                new_sequence.append([stripped_line])
        window[Keys.FILES_PATH].update(values=new_sequence)
    except:
        sg.popup_error("There was an error while loading the sequence")