#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the receiver dummy for the optical communications test
and interact with it.
"""

import os

import FreeSimpleGUI as sg

from gui_data import GUIData
from utils import *
from layout import *
from keys import *
from callbacks import *


# Callbacks must be able to receive three parameters: window, values and a GUIData object.
EVENT_CALLBACK_DICT = {
  Keys.SAVE: save_message,
  Keys.DIR_NAME: lambda w, v, data: data.setDirectoryPath(v[Keys.DIR_NAME]),
  Keys.EXP_SAVE_DIR: lambda w, v, data: data.setDirectoryPath(v[Keys.EXP_SAVE_DIR]),
  Keys.GET_EXPERIMENT: get_experiment_callback,
  Keys.STOP: lambda w, v, data: data.setReceivingMessage(False),
  Keys.RECEIVE: lambda w, v, data: data.setReceivingMessage(True),
  Keys.CLEAN: lambda w, v, data: w[Keys.MESSAGE].update(value=data.setMessage(""))
}

EVENT_CALLBACK_DICT.update(dict.fromkeys(VISIBILITY_KEYS, visibility_callback))

def main():
    """Main function to start the execution of the receiver program."""

    data = GUIData("", None, False)
    window = define_gui_layout()

    while True:  # Event Loop
        event, values = window.read(timeout=1)
        #if event != "__TIMEOUT__":
        #    print(event, values)
        if event == sg.WIN_CLOSED or event in EXIT_KEYS:
            break
        
        if event in EVENT_CALLBACK_DICT:
            EVENT_CALLBACK_DICT[event](window, values, data) 

        if values[Keys.TOGGLE_SEC_SHOW_TEXT] and data.receiving_message:
            data.message = receive_message()
            window[Keys.MESSAGE].update(value=data.message)

            # ToDo: Change from deactivating the receiving mode to a timeout to update
            #  the message continuously
            data.receiving_message = False

    window.close()

if __name__ == "__main__":
    main()
