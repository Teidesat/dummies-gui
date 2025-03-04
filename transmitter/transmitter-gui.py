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
  Keys.LOAD_SETTINGS.value: load_settings,
  # Directory path filled
  Keys.DIR_PATH.value: lambda window, values: window[Keys.FILES_LIST.value]
                                        .update(get_files_from_path(values[Keys.DIR_PATH.value])),
  Keys.FILES_PATH.value: lambda window, values: window[Keys.FILES_LIST.value]
                                          .update(values[Keys.FILES_PATH.value]),
  # ToDo: Send a request to stop the optical communications
  Keys.STOP.value: lambda window, values: sg.popup_quick_message(
                                        "Not implemented yet, work in progress.",
                                        auto_close_duration=2,
                                        background_color="yellow",
                                        text_color="black"
                                    ),
  Keys.SEND.value: send_callback
}

EVENT_CALLBACK_DICT.update(dict.fromkeys([Keys.TOGGLE_PLAIN_TEXT.value, Keys.TOGGLE_FILE.value,
                                          Keys.TOGGLE_EXP.value, Keys.TOGGLE_SEQ.value], update_visibility))


def main():
    """Main function to start the execution of the transmitter program."""
    main_window = define_main_gui_layout()
    update_settings(DEFAULT_SETTINGS, main_window)
    # Since Chooser Buttons like FileSaveAs are not considered events, this variables tracks changes
    previous_save_path = None
    while True:  # Event Loop
        event, values = main_window.read(timeout=1)
        # print(event, values, flush=DEBUG_MODE)
        if event == sg.WIN_CLOSED or event == Keys.EXIT.value:
            break

        if previous_save_path != values[Keys.SAVE_SETTINGS.value]:
            previous_save_path = values[Keys.SAVE_SETTINGS.value]
            save_settings(values, values[Keys.SAVE_SETTINGS.value])

        if event in EVENT_CALLBACK_DICT:
            EVENT_CALLBACK_DICT[event](main_window, values)

        # ToDo: Figure out how to add this to the callback dictionary. 
        # As an alternative, call this function together with the events that trigger it.
        if (
            event.startswith("-PARAM")
            or event.endswith("SETTINGS-")
            or event == "-TOGGLE_SEC-EXP-"
            or event == "-SEND-"
        ):
            # Update the experiment id based on the currently provided settings
            main_window[Keys.EXP_ID.value].update(
                get_current_experiment_id(get_current_settings(values))
            )

    main_window.close()

if __name__ == "__main__":
    main()
