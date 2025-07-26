#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToDo: Add a description of this module.
"""

import FreeSimpleGUI as Fsg

from .popup_keys import Keys


def define_gui_layout():
    """Function to define the GUI layout of the popup window."""

    bar_size = (25, 15)
    main_layout = [
        [
            Fsg.Text("Sending "),
            Fsg.Text("experiment_id", key=Keys.EXP_ID),
        ],
        [
            Fsg.Text("Current experiment progress: "),
            Fsg.Text("1 out of 10", key=Keys.EXP_PROGRESS_TEXT),
        ],
        [
            Fsg.ProgressBar(
                10,
                size=bar_size,
                key=Keys.CURRENT_EXP_PROGRESS,
                expand_x=True,
            )
        ],
        [
            Fsg.Text("Current sequence progress: "),
            Fsg.Text("1 out of 10", key=Keys.SEQ_PROGRESS_TEXT),
        ],
        [
            Fsg.ProgressBar(
                10,
                size=bar_size,
                key=Keys.CURRENT_SEQUENCE_PROGRESS,
                expand_x=True,
            )
        ],
        [
            Fsg.Button("Skip current experiment", key=Keys.SKIP),
            Fsg.Button("Stop communication", key=Keys.STOP),
        ],
    ]

    main_window = Fsg.Window(
        "Communication progress",
        main_layout,
        finalize=True,
        grab_anywhere_using_control=False,
        icon="../../img/window_icon.png",
        resizable=False,
    )

    return main_window
