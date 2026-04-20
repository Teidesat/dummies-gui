#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Various utility functions used throughout the program.
"""

import os
import re

import FreeSimpleGUI as Fsg
from requests import get as get_request
from dotenv import load_dotenv

from layout import DEFAULT_EXP_ID
from keys import Keys
load_dotenv()

RECEIVER_SERVER_BASE_URL = os.getenv("RECEIVER_SERVER_BASE_URL")


def receive_message():
    """Function to receive the message from the transmitter server."""

    response = get_request(f"{RECEIVER_SERVER_BASE_URL}/message")

    if response.status_code != 200:
        raise ConnectionError(
            f"Failed to receive message from server with error code {response.status_code}."
        )

    return response.text


def get_experiment():
    """
    Function to retrieve an experiment from the receiver's server
    """

    response = get_request(
        f"{RECEIVER_SERVER_BASE_URL}/experiment",
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        print(response)
        exit(-1)

    try:
        data = response.json()

        exp_id = data["id"]
        settings = parse_id(exp_id)
        messages = data["messages"]

        return exp_id, settings, messages

    except:  # ToDo: Catch the exception with the explicit error type
        Fsg.popup("There is no experiment ready")
        return DEFAULT_EXP_ID, None, []


def get_buffer_size():
    """
    Function to retrieve the size of the experiment buffer from the receiver's server
    """

    response = get_request(
        f"{RECEIVER_SERVER_BASE_URL}/buffer_size",
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        exit(-1)

    return response.text


def parse_id(experiment_id: str):
    """
    Parses the given experiment id to retrieve the parameters and the return them as settings.
    """

    number_re = R"\d+(?:\.\d+)?"
    match = re.fullmatch(
        Rf"CO_D({number_re})-A({number_re})-I({number_re})-F({number_re})-L({number_re})-Mm",
        experiment_id,
    )

    if match is None:
        raise ValueError(f"Unexpected error when parsing the ID '{experiment_id}'")

    match = match.groups()
    print(match)

    settings = {
        "distance": match[0],
        "angle": match[1],
        "intensity": match[2],
        "frequency": match[3],
        "batch": match[4],
    }

    return settings


def assert_directory(directory_path):
    """
    Function to check if the directory exists. Displays an error message if
    there is an error and returns false. Returns true otherwise.
    """

    if directory_path == "":
        Fsg.popup_error("ERROR: The directory path is empty.")
        return False

    if not os.path.isdir(directory_path):
        Fsg.popup_error(
            f'ERROR: The provided directory "{directory_path}" is not a directory.'
        )
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


def update_params(window: Fsg.Window, settings):
    """
    Function to update the parameters from the experiment section.
    Writes 0 if the settings param is None
    """

    window[Keys.DISTANCE_PARAM].update(
        settings["distance"] if settings is not None else 0
    )
    window[Keys.ANGLE_PARAM].update(settings["angle"] if settings is not None else 0)
    window[Keys.INTENSITY_PARAM].update(
        settings["intensity"] if settings is not None else 0
    )
    window[Keys.FREQUENCY_PARAM].update(
        settings["frequency"] if settings is not None else 0
    )
    window[Keys.BATCH_PARAM].update(settings["batch"] if settings is not None else 0)


def ascii_to_binary(ascii_str: str):
    """
    Transforms the given ASCII string to a binary string
    """
    try:
        result = ""

        for char in ascii_str:
            result += format(ord(char), "08b")

        return result

    except:  # ToDo: Catch the exception with the explicit error type
        Fsg.popup_error(f"Failed to transform {ascii_str} into a binary string")
        return ascii_str


def binary_to_ascii(binary_str: str):
    """
    Transforms the given binary string to ASCII
    """

    try:
        result = ""

        for ind in range(0, len(binary_str), 8):
            binary_char = binary_str[ind : ind + 8]
            ascii_code = int(binary_char, 2)
            ascii_char = format(ascii_code, "c")
            result += ascii_char

        return result

    except:  # ToDo: Catch the exception with the explicit error type
        Fsg.popup_error(f"Failed to transform {binary_str} into an ASCII string")
        return binary_str
