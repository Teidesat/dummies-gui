"""
  Defines the structure and style of PySimpleGUI's elements
"""

import FreeSimpleGUI as sg

from keys import Keys

def define_gui_layout():
    """Function to define the GUI layout."""

    sec_show_text_visible = True
    sec_save_file_visible = False
    sec_experiment_visible = False
    assert (sec_show_text_visible or sec_save_file_visible or sec_experiment_visible) == True
    assert (sec_show_text_visible + sec_save_file_visible + sec_experiment_visible) == 1

    # ---------------------------------------------------------------------------------

    show_text_section_layout = [
        [sg.Text("Message:")],
        [sg.Multiline(size=(50, 10), disabled=True, key=Keys.MESSAGE)],
        [
            sg.Button("Receive", key=Keys.RECEIVE),
            sg.Button("Stop", key=Keys.STOP),
            sg.Button("Clean", key=Keys.CLEAN),
            sg.Button("Exit", key=Keys.EXIT_1),
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
            sg.Button("Exit", key=Keys.EXIT_2),
        ],
    ]

    params_layout = [[
        sg.Text("Distance:"), sg.Text("0"),
        sg.Text("Angle:"), sg.Text("0"),
        sg.Text("Intensity:"), sg.Text("0"),
        sg.Text("Frequency:"), sg.Text("0"),
        sg.Text("Message Batch:"), sg.Text("0")
    ]]

    experiment_section_layout = [
        [sg.Text("Experiment ID:"), sg.Text("CO_Dd-Aa-Ii-Ff-Ll-Mm", key=Keys.EXPERIMENT_ID)],
        [sg.Text("Messages:")],
        [sg.Table(values=[], headings=["ID", "Message"], enable_events=True, expand_x=True, key=Keys.EXPERIMENT_TABLE,
                  background_color="white", text_color="black", alternating_row_color="lightgray")],
        [sg.Frame("Parameters", layout=params_layout, visible=True)],
        [
            sg.Text("Save Directory:"),
            sg.In(size=30, enable_events=True, key=Keys.EXP_SAVE_DIR),
            sg.FolderBrowse(),
        ],
        [sg.Button("Get experiment", key= Keys.GET_EXPERIMENT), sg.Button("Exit", key=Keys.EXIT_3)]
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
            " Experiment",
            "Radio",
            default=sec_experiment_visible,
            enable_events=True,
            key=Keys.TOGGLE_SEC_EXPERIMENT,
        )
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
            experiment_section_layout,
            key=Keys.SEC_EXPERIMENT,
            visible=sec_experiment_visible
        )
    ]

    # ---------------------------------------------------------------------------------

    main_layout = [
        radio_selector_layout,
        sub_sections_layout,
    ]

    window = sg.Window("Receiver", main_layout)
    return window