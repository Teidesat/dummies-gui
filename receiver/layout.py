"""
  Defines the structure and style of PySimpleGUI's elements
"""

import FreeSimpleGUI as sg

from keys import Keys

def define_gui_layout():
    """Function to define the GUI layout."""

    sec_show_text_visible = True
    sec_save_file_visible = False
    sec_sequence_visible = False

    assert (sec_show_text_visible or sec_save_file_visible or sec_sequence_visible) == True
    assert (sec_show_text_visible + sec_save_file_visible + sec_sequence_visible) == 1

    # ---------------------------------------------------------------------------------

    show_text_section_layout = [
        [sg.Text("Message:")],
        [sg.Multiline(size=(50, 10), disabled=True, key=Keys.MESSAGE)],
        [
            sg.Button("Receive", key=Keys.RECEIVE),
            sg.Button("Stop", key=Keys.STOP),
            sg.Button("Clean", key=Keys.CLEAN),
        ],
    ]

    save_file_section_layout = [
        [
            sg.Text("Directory:"),
            sg.In(size=30, enable_events=True, key=Keys.DIR_NAME),
            sg.FolderBrowse(),
        ],
        [
            sg.Text("File name:"),
            sg.In(default_text="", size=30, key=Keys.FILE_NAME),
        ],
        [
            sg.Text(
                "Error: The provided path is not a valid directory.",
                text_color="red",
                background_color="black",
                visible=False,
                key=Keys.PATH_ERROR_MSG,
            ),
        ],
        [
            sg.Button("Save to file", key=Keys.SAVE),
        ],
    ]
    table = sg.Table(values=[], headings=["ID", "Messages"], display_row_numbers=False, justification="center", 
                  enable_events=True, size=(50, 10), expand_x=True, key=Keys.EXPERIMENTS, 
                  background_color="white", text_color="black", alternating_row_color="lightgray", auto_size_columns=True)
    sequence_section_layout = [
        
        [
            sg.Text("Files:")
        ],
        [
            table
        ],
        [
            sg.Button("Receive", key=Keys.RECEIVE_SEQUENCE),
            sg.Button("Remove Message(s)", key=Keys.REMOVE_SELECTED_FILES), 
            sg.Button("Save all", key=Keys.SAVE_ALL)
        ]
    ]

    # ---------------------------------------------------------------------------------

    radio_selector_layout = [
        sg.Radio(
            " Show text",
            "Radio",
            default=sec_show_text_visible,
            enable_events=True,
            key=Keys.TOGGLE_SEC_SHOW_TEXT,
        ),
        sg.Radio(
            " Save to file",
            "Radio",
            default=sec_save_file_visible,
            enable_events=True,
            key=Keys.TOGGLE_SEC_SAVE_FILE,
        ),
        sg.Radio(
            " Sequence",
            "Radio",
            default=sec_sequence_visible,
            enable_events=True,
            key=Keys.TOGGLE_SEC_SEQUENCE,
        ),
    ]

    sub_sections_layout = [
        sg.Column(
            show_text_section_layout,
            key=Keys.SEC_SHOW_TEXT,
            visible=sec_show_text_visible,
        ),
        sg.Column(
            save_file_section_layout,
            key=Keys.SEC_SAVE_FILE,
            visible=sec_save_file_visible,
        ),
        sg.Column(
            sequence_section_layout,
            key=Keys.SEC_SEQUENCE,
            visible=sec_sequence_visible,
        ),
    ]
    
    common_elements_layout = [
        [
            sg.Push(),
            sg.Button("Exit", key=Keys.EXIT),
            sg.Push()
        ],
    ]

    # ---------------------------------------------------------------------------------

    main_layout = [
        radio_selector_layout,
        sub_sections_layout,
        common_elements_layout
    ]

    window = sg.Window("Receiver", main_layout)
    return window