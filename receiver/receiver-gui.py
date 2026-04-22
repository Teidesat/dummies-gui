#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the receiver dummy for the optical communications test
and interact with it.
"""

import time

import FreeSimpleGUI as Fsg

from callbacks import (
    save_message,
    receive,
    get_experiment_callback,
    receive_sequence,
    toggle_recording,
    transform_binary_ascii,
    visibility_callback,
)
from gui_data import GUIData
from keys import Keys, VISIBILITY_KEYS
from layout import define_gui_layout


# Callbacks must be able to receive three parameters: window, values and a GUIData object.
EVENT_CALLBACK_DICT = {
    Keys.SAVE: save_message,
    Keys.RECEIVE: receive,
    Keys.DIR_NAME: lambda w, v, data: data.set_directory_path(v[Keys.DIR_NAME]),
    Keys.EXP_SAVE_DIR: lambda w, v, data: data.set_directory_path(v[Keys.EXP_SAVE_DIR]),
    Keys.GET_EXPERIMENT: get_experiment_callback,
    Keys.STOP: lambda w, v, data: data.set_receiving_message(False),
    Keys.CLEAN: lambda w, v, data: w[Keys.MESSAGE].update(value=data.set_message("")),
    Keys.SEQ_CLEAN: lambda w, v, data: w[Keys.SEQUENCES_TABLE].update(values=[]),
    Keys.RECEIVE_SEQUENCE: receive_sequence,
    Keys.RECORD: toggle_recording,
    Keys.USE_BINARY: transform_binary_ascii,
}

EVENT_CALLBACK_DICT.update(dict.fromkeys(VISIBILITY_KEYS, visibility_callback))


def main():
    """Main function to start the execution of the receiver program."""
    last_receive_time = 0
    receive_interval = 2.0

    data = GUIData("", None, False)
    window = define_gui_layout()

    while True:  # Event Loop
        event, values = window.read(timeout=1)
        # if event != "__TIMEOUT__":

        if event == Fsg.WIN_CLOSED or event == Keys.EXIT:
            break

        if event in EVENT_CALLBACK_DICT:
            EVENT_CALLBACK_DICT[event](window, values, data)

        if (time.time() - last_receive_time) > receive_interval:
            if data.receiving_message:
                receive_sequence(window, values, data)
                last_receive_time = time.time()
            elif data.recording_enabled:
                receive(window, values, data)
                last_receive_time = time.time()

    if data.recording_enabled:
        data.stop_recording()

    window.close()


if __name__ == "__main__":
    main()
