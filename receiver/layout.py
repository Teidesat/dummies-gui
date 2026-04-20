#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines the structure and style of PySimpleGUI's elements.
"""

import os

import FreeSimpleGUI as Fsg

from keys import Keys

DEFAULT_EXP_ID = "CO_Dd-Aa-Ii-Ff-Ll-Mm"


# ToDo: split this function into smaller dedicated functions
def define_gui_layout():
    """Function to define the GUI layout."""

    sec_show_text_visible = True
    sec_save_file_visible = False
    sec_experiment_visible = False
    sec_sequence_visible = False

    assert (  # At least one section must be visible
        sec_show_text_visible
        or sec_save_file_visible
        or sec_experiment_visible
        or sec_sequence_visible
    ) == True

    assert (  # Only one section can be visible at a time
        sec_show_text_visible
        + sec_save_file_visible
        + sec_experiment_visible
        + sec_sequence_visible
    ) == 1

    # ---------------------------------------------------------------------------------

    show_text_section_layout = [
        [Fsg.Text("Message:")],
        [Fsg.Multiline(size=(50, 10), disabled=True, key=Keys.MESSAGE)],
        [
            Fsg.Push(),
            Fsg.Checkbox(
                "Use binary",
                default=True,
                key=Keys.USE_BINARY,
                enable_events=True,
            ),
            Fsg.Push(),
        ],
        [
            Fsg.Push(),
            Fsg.Button("Receive", key=Keys.RECEIVE),
            Fsg.Button("Record", key=Keys.RECORD),
            Fsg.Button("Clean", key=Keys.CLEAN),
            Fsg.Push(),
        ],
    ]

    save_file_section_layout = [
        [
            Fsg.Text("Directory:"),
            Fsg.In(size=30, enable_events=True, key=Keys.DIR_NAME),
            Fsg.FolderBrowse(),
        ],
        [
            Fsg.Text("File name:"),
            Fsg.In(default_text="", size=30, key=Keys.FILE_NAME),
        ],
        [
            Fsg.Text(
                "Error: The provided path is not a valid directory.",
                text_color="red",
                background_color="black",
                visible=False,
                key=Keys.PATH_ERROR_MSG,
            ),
        ],
        [
            Fsg.Push(),
            Fsg.Button("Save to file", key=Keys.SAVE),
            Fsg.Push(),
        ],
    ]
    table = Fsg.Table(
        values=[],
        headings=["ID", "Messages"],
        display_row_numbers=False,
        justification="center",
        enable_events=True,
        num_rows=20,  # Increase height (rows displayed)
        expand_x=True,  # Allows it to stretch horizontally
        expand_y=True,  # Allows it to stretch vertically
        key=Keys.SEQUENCES_TABLE,
        background_color="white",
        text_color="black",
        alternating_row_color="lightgray",
        auto_size_columns=False,  # Disable auto-sizing to manually set column widths
        col_widths=[40, 30],  # Make the "ID" column wider than "Messages"
    )

    default_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "message-batches"
    )

    if not os.path.isdir(default_folder):
        default_folder = os.getcwd()

    sequence_section_layout = [
        [Fsg.Text("Files:")],
        [
            # Wrap table in a column for better resizing
            Fsg.Column([[table]], expand_x=True, expand_y=True)
        ],
        [
            Fsg.Push(),
            Fsg.Button("Receive", key=Keys.RECEIVE_SEQUENCE),
            Fsg.Button("Stop", key=Keys.STOP),
            Fsg.Button("Clean", key=Keys.SEQ_CLEAN),
            Fsg.Push(),
        ],
        [
            Fsg.Text("Save Directory:"),
            Fsg.In(
                size=(50, 1),
                enable_events=True,
                key=Keys.SEQ_SAVE_DIR,
                default_text=default_folder,
            ),  # Widen input box
            Fsg.FolderBrowse(),
        ],
    ]

    params_layout = [
        [
            Fsg.Column(
                [
                    [Fsg.Text("Distance:"), Fsg.Text("0", key=Keys.DISTANCE_PARAM)],
                    [Fsg.Text("Angle:"), Fsg.Text("0", key=Keys.ANGLE_PARAM)],
                    [Fsg.Text("Intensity:"), Fsg.Text("0", key=Keys.INTENSITY_PARAM)],
                    [Fsg.Text("Frequency:"), Fsg.Text("0", key=Keys.FREQUENCY_PARAM)],
                    [Fsg.Text("Message Batch:"), Fsg.Text("0", key=Keys.BATCH_PARAM)],
                ]
            ),
        ]
    ]

    experiment_section_layout = [
        [Fsg.Text("Experiment ID:"), Fsg.Text(DEFAULT_EXP_ID, key=Keys.EXPERIMENT_ID)],
        [Fsg.Text("Messages:")],
        [
            Fsg.Table(
                values=[],
                headings=["ID", "Message"],
                enable_events=True,
                expand_x=True,
                key=Keys.EXPERIMENT_TABLE,
                background_color="white",
                text_color="black",
                alternating_row_color="lightgray",
            )
        ],
        [Fsg.Frame("Parameters", layout=params_layout, visible=True)],
        [
            Fsg.Text("Save Directory:"),
            Fsg.In(size=30, enable_events=True, key=Keys.EXP_SAVE_DIR),
            Fsg.FolderBrowse(),
        ],
        [
            Fsg.Push(),
            Fsg.Button("Get experiment", key=Keys.GET_EXPERIMENT),
            Fsg.Push(),
        ],
    ]

    # ---------------------------------------------------------------------------------

    radio_selector_layout = [
        Fsg.Radio(
            " Show text",
            "Radio",
            default=sec_show_text_visible,
            enable_events=True,
            key=Keys.TOGGLE_SEC_SHOW_TEXT,
        ),
        Fsg.Radio(
            " Save to file",
            "Radio",
            default=sec_save_file_visible,
            enable_events=True,
            key=Keys.TOGGLE_SEC_SAVE_FILE,
        ),
        Fsg.Radio(
            " Experiment",
            "Radio",
            default=sec_experiment_visible,
            enable_events=True,
            key=Keys.TOGGLE_SEC_EXPERIMENT,
        ),
        Fsg.Radio(
            " Sequence",
            "Radio",
            default=sec_sequence_visible,
            enable_events=True,
            key=Keys.TOGGLE_SEC_SEQUENCE,
        ),
    ]

    sub_sections_layout = [
        Fsg.Column(
            show_text_section_layout,
            key=Keys.SEC_SHOW_TEXT,
            visible=sec_show_text_visible,
        ),
        Fsg.Column(
            save_file_section_layout,
            key=Keys.SEC_SAVE_FILE,
            visible=sec_save_file_visible,
        ),
        Fsg.Column(
            experiment_section_layout,
            key=Keys.SEC_EXPERIMENT,
            visible=sec_experiment_visible,
        ),
        Fsg.Column(
            sequence_section_layout,
            key=Keys.SEC_SEQUENCE,
            visible=sec_sequence_visible,
        ),
    ]

    common_elements_layout = [
        [
            Fsg.Push(),
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

    window = Fsg.Window("Receiver", main_layout)
    return window
