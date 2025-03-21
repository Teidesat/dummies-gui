"""
  Various utility functions used throughout the program
"""
import os
import FreeSimpleGUI as sg
import re

from keys import *
from requests import get as get_request

def receive_message():
    """Function to receive the message from the transmitter server."""

    # ToDo: Change request address and endpoint to receive the message from the receiver
    #  dummy's server instead of the transmitter server, it's currently the same server
    #  to test the communication between the two dummies GUIs.
    response = get_request("http://transmitter-server:5000/get_message_data")

    if response.status_code != 200:
        raise ConnectionError(
            f"Failed to receive message from server with error code {response.status_code}."
        )

    return response.text

def get_experiment():
    """
    Function to retrieve an experiment from the receiver's server
    """
    # id = "CO_D60-A45-I3-F90-L1-Mm"
    #settings = {
    #    "distance": "60",
    #    "angle": "45",
    #    "intensity": "3",
    #    "frequency": "90",
    #    "batch": "1"
    #}
    data = get_request("http://receiver-server:5000/experiment")
    if data.status_code != 200:
        print(data)
        exit(-1)
    data = data.json()
    id = data["id"]
    settings = parse_id(id)
    messages = data["messages"]
    return id, settings, messages

def parse_id(experiment_id: str):
    """
    Parses the given experiment id to retrieve the parameters and the return them as settings.
    """
    number_re = R"\d+(?:\.\d+)?"
    match = re.fullmatch(fR"CO_D({number_re})-A({number_re})-I({number_re})-F({number_re})-L({number_re})-Mm",
                         experiment_id)
    if match == None:
        raise ValueError(f"Unexpected error when parsing the ID '{experiment_id}'")
    match = match.groups()
    print(match)
    settings = {
        "distance": match[0],
        "angle": match[1],
        "intensity": match[2],
        "frequency": match[3],
        "batch": match[4]
    }
    return settings

def assert_directory(directory_path):
    """
    Function to check if the directory exists. Displays an error message if
    there is an error and returns false. Returns true otherwise.
    """
    if directory_path == "":
        sg.popup_error("ERROR: The directory path is empty.")
        return False
    if not os.path.isdir(directory_path):
        sg.popup_error(f"ERROR: The provided directory \"${directory_path}\" is not a directory.")
        return False
    return True

def save_messages_to_csv(messages, directory, name):
    """
    Function to save messages from an experiment to a single csv.

    'messages' is used under the assumption is a list formed by lists of two
    elements: id and message, in that order.
    """
    name = name + ".csv"
    path = os.path.join(directory, name)
    with open(path, "w") as file:
        messages = map(lambda val: ",".join(val), messages)
        messages = "\n".join(messages)
        file.write(messages)

def update_params(window: sg.Window, settings):
    """
    Function to update the parameters from the experiment section.
    """
    window[Keys.DISTANCE_PARAM].update(settings["distance"])
    window[Keys.ANGLE_PARAM].update(settings["angle"])
    window[Keys.INTENSITY_PARAM].update(settings["intensity"])
    window[Keys.FREQUENCY_PARAM].update(settings["frequency"])
    window[Keys.BATCH_PARAM].update(settings["batch"])