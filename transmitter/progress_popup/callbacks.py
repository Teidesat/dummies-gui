#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToDo: Add a description of this module.
"""

from requests import get as get_request

import FreeSimpleGUI as Fsg

from .progress_data import ProgressData
from .popup_keys import Keys

BASE_URL = "http://transmitter-server:5000/"


def change_to_next_experiment(window: Fsg.Window, values, data: ProgressData):
    """ToDo: Add a description of this function."""

    endpoint = "/next_experiment"
    response = get_request(BASE_URL + endpoint)
    # ToDo: Handle the response appropriately

    update_window(window, data)


def stop_communication():
    """ToDo: Add a description of this function."""

    endpoint = "/stop_communication"
    response = get_request(BASE_URL + endpoint)
    # ToDo: Handle the response appropriately


def update_window(window: Fsg.Window, data: ProgressData):
    """ToDo: Add a description of this function."""

    endpoint = "/current_status"
    response = get_request(BASE_URL + endpoint)
    print(response)
    # ToDo: Handle the response appropriately

    received_data = response.json()
    print(received_data)

    experiment_id = received_data["experiment_id"]
    experiments = received_data["experiments"]
    messages = received_data["messages"]

    data.set_data(messages, experiments, experiment_id)
    experiment_id_str, messages_str, experiments_str = data.get_formatted(
        messages, experiments
    )

    window[Keys.EXP_ID].update(experiment_id_str)
    window[Keys.CURRENT_EXP_PROGRESS].update(
        current_count=data.total_messages - messages + 1, max=data.total_messages
    )
    window[Keys.CURRENT_SEQUENCE_PROGRESS].update(
        current_count=data.total_experiments - experiments + 1,
        max=data.total_experiments,
    )
    window[Keys.SEQ_PROGRESS_TEXT].update(experiments_str)
    window[Keys.EXP_PROGRESS_TEXT].update(messages_str)
