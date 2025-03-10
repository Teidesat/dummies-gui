"""
File defining the layout of the GUI
"""

import PySimpleGUI as sg
from utils import retrieve_combo_values
from keys import *

def define_main_gui_layout():
    """Function to define the GUI layout of the main window."""

    sec_plain_text_visible = True
    sec_exp_visible = False
    sec_file_visible = False
    sec_seq_visible = False

    assert (sec_plain_text_visible or sec_exp_visible or sec_file_visible or sec_seq_visible) == True
    assert (sec_plain_text_visible + sec_exp_visible + sec_file_visible + sec_seq_visible) == 1

    # ---------------------------------------------------------------------------------

    standard_settings_labels = [
        [
            sg.Text("Dummies distance:", expand_x=True),
        ],
        [
            sg.Text("Transmitter angle:", expand_x=True),
        ],
        [
            sg.Text("LEDs intensity:", expand_x=True),
        ],
        [
            sg.Text("Blinking frequency:", expand_x=True),
        ],
    ]

    standard_settings_inputs = [
        [
            sg.Combo(
                values=retrieve_combo_values("distance"),
                size=5,
                enable_events=True,
                key=Keys.PARAM_DUMMY_DISTANCE,
            ),
            sg.Text("m"),
        ],
        [
            sg.Combo(
                values=retrieve_combo_values("angle"),
                size=5,
                enable_events=True,
                key=Keys.PARAM_TRANSMITTER_ANGLE,
            ),
            sg.Text("º"),
        ],
        [
            sg.Combo(
                values=retrieve_combo_values("power"),
                size=5,
                enable_events=True,
                key=Keys.PARAM_LED_INTENSITY,
            ),
            sg.Text("A"),
        ],
        [
            sg.Combo(
                values=retrieve_combo_values("frecuency"),
                size=5,
                enable_events=True,
                key=Keys.PARAM_BLINKING_FREQUENCY,
            ),
            sg.Text("Hz"),
        ],
    ]

    standard_settings_layout = [
        [
            sg.Column(standard_settings_labels),
            sg.Column(standard_settings_inputs),
        ]
    ]

    # ---------------------------------------------------------------------------------

    experiment_extra_settings_labels = [
        [
            sg.Text("Experiment Id:", expand_x=True),
        ],
        [
            sg.Text("Messages batch:", expand_x=True),
        ],
    ]

    experiment_extra_settings_inputs = [
        [
            sg.Text(text="CO_Dd-Aa-Ii-Ff-Cc-Mm", key=Keys.EXP_ID),
        ],
        [
            sg.In(
                size=5,
                enable_events=True,
                key=Keys.PARAM_MESSAGES_BATCH,
            ),
        ],
    ]

    experiment_extra_settings_layout = [
        [
            sg.Column(experiment_extra_settings_labels),
            sg.Column(experiment_extra_settings_inputs),
        ]
    ]

    # ---------------------------------------------------------------------------------

    plain_text_section_layout = [
        [sg.Text("Message:")],
        [sg.Multiline(size=(50, 10), key=Keys.MESSAGE)],
    ]

    file_section_layout = [
        [
            sg.Text("File:"),
            sg.In(size=30, enable_events=True, key=Keys.DIR_PATH),
            sg.FolderBrowse(),
        ],
        [sg.Listbox(values=[], enable_events=True, size=(50, 10), key=Keys.FILES_LIST)],
    ]

    experiment_section_layout = experiment_extra_settings_layout

    sequence_section_layout = [
        
        [sg.Text("Files:")],
        [sg.Listbox(values=[], enable_events=True, size=(50, 10), expand_x=True, key=Keys.FILES_PATH, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
        [sg.Button("Add file(s)", key=Keys.NEW_FILES), sg.Button("Remove file(s)", key=Keys.REMOVE_SELECTED_FILES),
         sg.Button("Move file(s) up", key=Keys.MOVE_UP), sg.Button("Move file(s) down", key=Keys.MOVE_DOWN)] # Buttons to change the ordering of selected files.
        #[sg.Listbox(values=[], enable_events=True, size=(50, 10), key=Keys.FILES_LIST, visible=False)],
    ]
    # ---------------------------------------------------------------------------------

    radio_selector_layout = [
        [
            sg.Radio(
                " Plain text",
                "Radio",
                default=sec_plain_text_visible,
                enable_events=True,
                key=Keys.TOGGLE_PLAIN_TEXT,
            ),
            sg.Radio(
                " File",
                "Radio",
                default=sec_file_visible,
                enable_events=True,
                key=Keys.TOGGLE_FILE,
            ),
            sg.Radio(
                " Experiment",
                "Radio",
                default=sec_exp_visible,
                enable_events=True,
                key=Keys.TOGGLE_EXP,
            ),
            sg.Radio(
                " Sequence",
                "Radio",
                default=sec_seq_visible,
                enable_events=True,
                key=Keys.TOGGLE_SEQ,
            ),
        ],
    ]

    sub_sections_layout = [
        [
            sg.Column(
                plain_text_section_layout,
                key=Keys.SEC_PLAIN_TEXT,
                visible=sec_plain_text_visible,
            ),
            sg.Column(
                file_section_layout,
                key=Keys.SEC_FILE,
                visible=sec_file_visible,
            ),
            sg.Column(
                experiment_section_layout,
                key=Keys.SEC_EXP,
                visible=sec_exp_visible,
            ),
            sg.Column(
                sequence_section_layout,
                key=Keys.SEC_SEQ,
                visible=sec_seq_visible,
            ),
        ]
    ]

    common_elements_layout = [
        [
            sg.Column(standard_settings_layout),
        ],
        [
            sg.Button("Load settings", key=Keys.LOAD_SETTINGS),
            sg.FileSaveAs("Save settings", key=Keys.SAVE_SETTINGS, file_types=(
                ("JSON files", ".json"),
                ("ALL Files", ". *"),),
            )
        ],
        [
            sg.Button("Send", key=Keys.SEND),
            sg.Button("Stop", key=Keys.STOP),
            sg.Button("Exit", key=Keys.EXIT),
        ],
    ]

    # ---------------------------------------------------------------------------------

    main_layout = [
        radio_selector_layout,
        sub_sections_layout,
        common_elements_layout,
    ]

    main_window = sg.Window("Transmitter", main_layout, finalize=True)
    return main_window