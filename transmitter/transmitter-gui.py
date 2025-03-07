#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the transmitter dummy for the optical communications
test and interact with it.
"""

import json
import os
import sys

import PySimpleGUI as sg

from callbacks import *
from keys import *
from utils import *
from layout import define_main_gui_layout

DEFAULT_SETTINGS = {
    "dummy_distance": 3,
    "transmitter_angle": 0,
    "led_intensity": 0.5,
    "blinking_frequency": 30,
    "messages_batch": 1,
}

# Callbacks must be able to receive two parameters: window and values.
EVENT_CALLBACK_DICT = {
  Keys.LOAD_SETTINGS: load_settings_callback,
  # Directory path filled
  Keys.DIR_PATH: lambda window, values: window[Keys.FILES_LIST]
                                        .update(get_files_from_path(values[Keys.DIR_PATH])),
  Keys.FILES_PATH: lambda window, values: window[Keys.FILES_LIST]
                                          .update(values[Keys.FILES_PATH]),
  # ToDo: Send a request to stop the optical communications
  Keys.STOP: lambda window, values: sg.popup_quick_message(
                                        "Not implemented yet, work in progress.",
                                        auto_close_duration=2,
                                        background_color="yellow",
                                        text_color="black"
                                    ),
  Keys.SEND: send_callback,
  Keys.NEW_FILES: add_files,
  Keys.REMOVE_SELECTED_FILES: remove_files
}

EVENT_CALLBACK_DICT.update(dict.fromkeys([Keys.TOGGLE_PLAIN_TEXT, Keys.TOGGLE_FILE,
                                          Keys.TOGGLE_EXP, Keys.TOGGLE_SEQ], update_visibility))


EVENT_CALLBACK_DICT.update(dict.fromkeys(PARAMETER_KEYS, 
                                         lambda window, values: window[Keys.EXP_ID].update(
                                            get_current_experiment_id(get_current_settings(window)))))

def main():
    """Main function to start the execution of the transmitter program."""
    main_window = define_main_gui_layout()
    update_settings(DEFAULT_SETTINGS, main_window)
    # Since Chooser Buttons like FileSaveAs are not considered events, this variables tracks changes
    previous_save_path = None
    while True:  # Event Loop
        event, values = main_window.read(timeout=1)
        # print(event, values, flush=DEBUG_MODE)
        if event == sg.WIN_CLOSED or event == Keys.EXIT:
            break

        if previous_save_path != values[Keys.SAVE_SETTINGS]:
            previous_save_path = values[Keys.SAVE_SETTINGS]
            save_settings(main_window, values[Keys.SAVE_SETTINGS])

        if event in EVENT_CALLBACK_DICT:
            EVENT_CALLBACK_DICT[event](main_window, values)

    main_window.close()

if __name__ == "__main__":
    main()
