#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToDo: Add a description of this module.
"""

from threading import Timer

import FreeSimpleGUI as Fsg

from .layout import define_gui_layout
from .popup_keys import Keys
from .callbacks import (
    change_to_next_experiment,
    stop_communication,
    update_window,
)
from .progress_data import ProgressData


EVENT_DICTIONARY = {
    Keys.SKIP: change_to_next_experiment,
}


def run_progress_window():
    """ToDo: Add a description of this function."""

    window = define_gui_layout()
    data = ProgressData()
    update_window(window, data)

    seconds_between_updates = 3
    update_timer = Timer(seconds_between_updates, lambda: 0)
    update_timer.start()

    while True:
        event, values = window.read(timeout=1)

        if update_timer.finished.is_set():
            update_window(window, data)
            update_timer = Timer(seconds_between_updates, lambda: 0)
            update_timer.start()

        if event == Fsg.TIMEOUT_EVENT:
            continue

        if event == Fsg.WIN_CLOSED or event == Keys.STOP:
            stop_communication()
            break

        if event in EVENT_DICTIONARY:
            EVENT_DICTIONARY[event](window, values, data)
        else:
            Fsg.popup_error(f"Unknown event ${event}")
            break

    update_timer.cancel()
    window.close()


if __name__ == "__main__":
    run_progress_window()
