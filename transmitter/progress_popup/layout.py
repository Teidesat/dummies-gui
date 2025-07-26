import FreeSimpleGUI as sg
from .popup_keys import Keys


def define_gui_layout():
    """Function to define the GUI layout of the popup window."""
    bar_size = (25, 15)
    main_layout = [
        [sg.Text("Sending "), sg.Text("experiment_id", key=Keys.EXP_ID)],
        [
            sg.Text("Current experiment progress: "),
            sg.Text("1 out of 10", key=Keys.EXP_PROGRESS_TEXT),
        ],
        [
            sg.ProgressBar(
                10, size=bar_size, key=Keys.CURRENT_EXP_PROGRESS, expand_x=True
            )
        ],
        [
            sg.Text("Current sequence progress: "),
            sg.Text("1 out of 10", key=Keys.SEQ_PROGRESS_TEXT),
        ],
        [
            sg.ProgressBar(
                10, size=bar_size, key=Keys.CURRENT_SEQUENCE_PROGRESS, expand_x=True
            )
        ],
        [
            sg.Button("Skip current experiment", key=Keys.SKIP),
            sg.Button("Stop communication", key=Keys.STOP),
        ],
    ]

    main_window = sg.Window(
        "Communication progress",
        main_layout,
        finalize=True,
        grab_anywhere_using_control=False,
        icon="../../img/window_icon.png",
        resizable=False,
    )
    return main_window
