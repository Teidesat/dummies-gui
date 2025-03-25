#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to start the execution of the receiver dummy for the optical communications test
and interact with it.
"""

import os

import time
import FreeSimpleGUI as sg

from gui_data import GUIData
from layout import *
from keys import *
from callbacks import *


# Callbacks must be able to receive three parameters: window, values and a GUIData object.
EVENT_CALLBACK_DICT = {
  Keys.SAVE: save_message,
  Keys.RECEIVE: receive,
  Keys.DIR_NAME: lambda w, v, data: data.setDirectoryPath(v[Keys.DIR_NAME]),
  Keys.EXP_SAVE_DIR: lambda w, v, data: data.setDirectoryPath(v[Keys.EXP_SAVE_DIR]),
  Keys.GET_EXPERIMENT: get_experiment_callback,
  Keys.STOP: lambda w, v, data: data.setReceivingMessage(False),
  Keys.CLEAN: lambda w, v, data: w[Keys.MESSAGE].update(value=data.setMessage("")),
  Keys.RECEIVE_SEQUENCE: receive_sequence,
  Keys.REMOVE_SELECTED_FILES: remove_files,
  Keys.SAVE_ALL: save_all
}

EVENT_CALLBACK_DICT.update(dict.fromkeys(VISIBILITY_KEYS, visibility_callback))

def main():
    """Main function to start the execution of the receiver program."""
    last_receive_time = 0
    receive_interval = 2
    
    data = GUIData("", None, False)
    window = define_gui_layout()
    while True:  # Event Loop
        event, values = window.read(timeout=1)
        #if event != "__TIMEOUT__":

        if event == sg.WIN_CLOSED or event == Keys.EXIT:
            break
        
        if event in EVENT_CALLBACK_DICT:
            EVENT_CALLBACK_DICT[event](window, values, data) 
            
        if data.receiving_message and (time.time() - last_receive_time > receive_interval):
            receive(window, values, data)
            last_receive_time = time.time()
            

    window.close()

if __name__ == "__main__":
    main()
