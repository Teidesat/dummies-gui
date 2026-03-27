#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File defining the layout of the GUI.
"""

import FreeSimpleGUI as Fsg

from utils import retrieve_combo_values
from keys import Keys


def define_main_gui_layout():
    """Function to define the GUI layout of the main window."""

    sec_plain_text_visible = True
    sec_file_visible = False
    sec_experiment_visible = False
    sec_sequence_visible = False

    assert (  # At least one section must be visible
        sec_plain_text_visible
        or sec_file_visible
        or sec_experiment_visible
        or sec_sequence_visible
    ) == True

    assert (  # Only one section can be visible at a time
        sec_plain_text_visible
        + sec_file_visible
        + sec_experiment_visible
        + sec_sequence_visible
    ) == 1

    # ---------------------------------------------------------------------------------

    standard_settings_labels = [
        [Fsg.Text("Dummies distance:", expand_x=True)],
        [Fsg.Text("Transmitter angle:", expand_x=True)],
        [Fsg.Text("LEDs intensity:", expand_x=True)],
        [Fsg.Text("Blinking frequency:", expand_x=True)],
    ]

    standard_settings_inputs = [
        [
            Fsg.Combo(
                values=retrieve_combo_values("distance"),
                size=5,
                enable_events=True,
                key=Keys.PARAM_DUMMY_DISTANCE,
            ),
            Fsg.Text("m"),
        ],
        [
            Fsg.Combo(
                values=retrieve_combo_values("angle"),
                size=5,
                enable_events=True,
                key=Keys.PARAM_TRANSMITTER_ANGLE,
            ),
            Fsg.Text("º"),
        ],
        [
            Fsg.Combo(
                values=retrieve_combo_values("power"),
                size=5,
                enable_events=True,
                key=Keys.PARAM_LED_INTENSITY,
            ),
            Fsg.Text("A"),
        ],
        [
            Fsg.Combo(
                values=retrieve_combo_values("frequency"),
                size=5,
                enable_events=True,
                key=Keys.PARAM_BLINKING_FREQUENCY,
            ),
            Fsg.Text("Hz"),
        ],
    ]

    standard_settings_layout = [
        [
            Fsg.Push(),
            Fsg.Column(standard_settings_labels),
            Fsg.Column(standard_settings_inputs),
            Fsg.Push(),
        ]
    ]

    # ---------------------------------------------------------------------------------

    experiment_extra_settings_labels = [
        [Fsg.Text("Experiment Id:", expand_x=True)],
        [Fsg.Text("Messages batch:", expand_x=True)],
    ]

    experiment_extra_settings_inputs = [
        [
            Fsg.Text(text="CO_Dd-Aa-Ii-Ff-Cc-Mm", key=Keys.EXP_ID),
        ],
        [
            Fsg.In(
                size=5,
                enable_events=True,
                key=Keys.PARAM_MESSAGES_BATCH,
            ),
        ],
    ]

    experiment_extra_settings_layout = [
        [
            Fsg.Push(),
            Fsg.Column(experiment_extra_settings_labels),
            Fsg.Column(experiment_extra_settings_inputs),
            Fsg.Push(),
        ]
    ]

    # ---------------------------------------------------------------------------------

    plain_text_section_layout = [
        [Fsg.Text("Message:")],
        [Fsg.Multiline(size=(50, 10), key=Keys.MESSAGE)],
    ]

    file_section_layout = [
        [
            Fsg.Text("File:"),
            Fsg.In(size=30, enable_events=True, key=Keys.DIR_PATH),
            Fsg.FolderBrowse(),
        ],
        [
            Fsg.Listbox(
                values=[], enable_events=True, size=(50, 10), key=Keys.FILES_LIST
            )
        ],
    ]

    experiment_section_layout = experiment_extra_settings_layout

    table = Fsg.Table(
        values=[],
        headings=["Experiment file"],
        display_row_numbers=True,
        justification="center",
        enable_events=True,
        size=(50, 10),
        expand_x=True,
        key=Keys.FILES_PATH,
        background_color="white",
        text_color="black",
        alternating_row_color="lightgray",
    )
    table.RowHeaderText = "Order"

    sequence_section_layout = [
        [Fsg.Text("Files:")],
        # [sg.Listbox(values=[], enable_events=True, size=(50, 10), expand_x=True, key=Keys.FILES_PATH, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
        [table],
        [
            Fsg.Button("Add file(s)", key=Keys.NEW_FILES),
            Fsg.Button("Remove file(s)", key=Keys.REMOVE_SELECTED_FILES),
            Fsg.Button("Move file(s) up", key=Keys.MOVE_UP),
            Fsg.Button("Move file(s) down", key=Keys.MOVE_DOWN),
        ],  # Buttons to change the ordering of selected files.
        # [sg.Listbox(values=[], enable_events=True, size=(50, 10), key=Keys.FILES_LIST, visible=False)],
    ]
    # ---------------------------------------------------------------------------------

    radio_selector_layout = [
        [
            Fsg.Push(),
            Fsg.Radio(
                " Plain text",
                "Radio",
                default=sec_plain_text_visible,
                enable_events=True,
                key=Keys.TOGGLE_PLAIN_TEXT,
            ),
            Fsg.Radio(
                " File",
                "Radio",
                default=sec_file_visible,
                enable_events=True,
                key=Keys.TOGGLE_FILE,
            ),
            Fsg.Radio(
                " Experiment",
                "Radio",
                default=sec_experiment_visible,
                enable_events=True,
                key=Keys.TOGGLE_EXP,
            ),
            Fsg.Radio(
                " Sequence",
                "Radio",
                default=sec_sequence_visible,
                enable_events=True,
                key=Keys.TOGGLE_SEQ,
            ),
            Fsg.Push(),
        ],
    ]

    sub_sections_layout = [
        [
            Fsg.Push(),
            Fsg.Column(
                plain_text_section_layout,
                key=Keys.SEC_PLAIN_TEXT,
                visible=sec_plain_text_visible,
            ),
            Fsg.Column(
                file_section_layout,
                key=Keys.SEC_FILE,
                visible=sec_file_visible,
            ),
            Fsg.Column(
                experiment_section_layout,
                key=Keys.SEC_EXP,
                visible=sec_experiment_visible,
            ),
            Fsg.Column(
                sequence_section_layout,
                key=Keys.SEC_SEQ,
                visible=sec_sequence_visible,
            ),
            Fsg.Push(),
        ]
    ]

    common_elements_layout = [
        [
            Fsg.Push(),
            # The pin function helps with visibility changes, shrinking the space the invisible element was occupying
            Fsg.pin(
                Fsg.Column(standard_settings_layout, key=Keys.STANDARD_SETTINGS),
            ),
            Fsg.Push(),
        ],
        [
            Fsg.Push(),
            Fsg.Button("Load settings", key=Keys.LOAD_SETTINGS),
            Fsg.FileSaveAs(
                "Save settings",
                key=Keys.SAVE_SETTINGS,
                file_types=(
                    ("JSON files", ".json"),
                    ("ALL Files", ". *"),
                ),
            ),
            Fsg.Push(),
        ],
        [
            Fsg.Push(),
            Fsg.Checkbox("Encode to binary", default=True, key=Keys.ENCODE_MESSAGE),
            Fsg.Push(),
        ],
        [
            Fsg.Push(),
            Fsg.Button("Send", key=Keys.SEND),
            Fsg.Button("Stop", key=Keys.STOP),
            Fsg.Button("Exit", key=Keys.EXIT),
            Fsg.Push(),
        ],
    ]

    # ---------------------------------------------------------------------------------

    main_layout = [
        radio_selector_layout,
        sub_sections_layout,
        common_elements_layout,
    ]

    main_window = Fsg.Window(
        "Transmitter",
        main_layout,
        finalize=True,
        grab_anywhere_using_control=False,
        icon="../img/window_icon.png",
    )

    return main_window
