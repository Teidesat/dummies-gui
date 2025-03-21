"""
  Define callbacks to be used in the main loop
"""
import os
import FreeSimpleGUI as sg

from utils import *
from keys import *
from gui_data import GUIData

def visibility_callback(window, values, data: GUIData):
  """
    Updates the visibility of the elements on the GUI
  """
  window[Keys.SEC_SHOW_TEXT].update(visible=values[Keys.TOGGLE_SEC_SHOW_TEXT])
  window[Keys.SEC_SAVE_FILE].update(visible=values[Keys.TOGGLE_SEC_SAVE_FILE])
  window[Keys.SEC_EXPERIMENT].update(visible=values[Keys.TOGGLE_SEC_EXPERIMENT])


def save_message(window, values, data: GUIData):
  """
    Saves the message in the selected file path
  """
  directory_path = data.directory_path
  if not os.path.isdir(directory_path):
    window[Keys.PATH_ERROR_MSG].update(visible=True)

  else:
    window[Keys.PATH_ERROR_MSG].update(visible=False)
    file_path = os.path.join(directory_path, values[Keys.FILE_NAME])

    # ToDo: Save received message to file
    print(file_path)

def get_experiment_callback(window: sg.Window, values, data: GUIData):
  save_directory = values[Keys.EXP_SAVE_DIR]
  if not assert_directory(save_directory):
    return
  id, settings = get_experiment()
  window[Keys.EXPERIMENT_ID].update(id)
  messages = get_messages(id)
  window[Keys.EXPERIMENT_TABLE].update(messages)
  save_messages_to_csv(messages, save_directory, id)