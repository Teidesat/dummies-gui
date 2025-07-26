import FreeSimpleGUI as sg
from threading import Timer
from .layout import define_gui_layout
from .popup_keys import Keys
from .callbacks import *
from .progress_data import ProgressData

EVENT_DICTIONARY = {
    Keys.SKIP: change_to_next_experiment,
}


def run_progress_window():
    window = define_gui_layout()
    data = ProgressData()
    update_window(window, data)
    SECONDS_BETWEEN_UPDATES = 3
    update_timer = Timer(SECONDS_BETWEEN_UPDATES, lambda: 0)
    update_timer.start()
    while True:
        event, values = window.read(timeout=1)
        if update_timer.finished.is_set():
            update_window(window, data)
            update_timer = Timer(SECONDS_BETWEEN_UPDATES, lambda: 0)
            update_timer.start()
        if event == sg.TIMEOUT_EVENT:
            continue
        if event == sg.WIN_CLOSED or event == Keys.STOP:
            stop_communication()
            break
        if event in EVENT_DICTIONARY:
            EVENT_DICTIONARY[event](window, values, data)
        else:
            sg.popup_error(f"Unknown event ${event}")
            break
    update_timer.cancel()
    window.close()


if __name__ == "__main__":
    run_progress_window()
