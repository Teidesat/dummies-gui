"""
  Define callbacks to be used in the main loop
"""
import os

from keys import *
from gui_data import GUIData

def visibility_callback(window, values, data: GUIData):
  """
    Updates the visibility of the elements on the GUI
  """
  window[Keys.SEC_SHOW_TEXT].update(visible=values[Keys.TOGGLE_SEC_SHOW_TEXT])
  window[Keys.SEC_SAVE_FILE].update(visible=values[Keys.TOGGLE_SEC_SAVE_FILE])


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
