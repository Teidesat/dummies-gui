"""
  Various utility functions used throughout the program
"""
import os
import FreeSimpleGUI as sg

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

    TODO: Currently mocking the server for UI development purposes, change to use the server.
    """
    id = "CO_D60-A45-I3-F90-L1-Mm"
    settings = {
        "distance": "60",
        "angle": "45",
        "intensity": "3",
        "frequency": "90",
        "batch": "1"
    }
    return id, settings

def get_messages(exp_id):
    """
    Function to retrieve the messages from a certain experiment.

    TODO: Currently mocking the server for UI development purposes, change to use the server. 
    Also, exp_id alone may not be enough to identify the experiment. A timestamp might be useful.
    """
    messages = [["1", "hello"],
                ["2", "teidesat"],
                ["3", "cubesat"],
                ["4", "hyperspace"]
                ]
    return messages

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