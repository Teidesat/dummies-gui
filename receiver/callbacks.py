"""
  Define callbacks to be used in the main loop
"""
import os
import json

from keys import *
from utils import *
from gui_data import GUIData

def visibility_callback(window, values, data: GUIData):
  """
    Updates the visibility of the elements on the GUI
  """
  window[Keys.SEC_SHOW_TEXT].update(visible=values[Keys.TOGGLE_SEC_SHOW_TEXT])
  window[Keys.SEC_SAVE_FILE].update(visible=values[Keys.TOGGLE_SEC_SAVE_FILE])
  window[Keys.SEC_SEQUENCE].update(visible=values[Keys.TOGGLE_SEC_SEQUENCE])


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


def receive_sequence(window, values, data: GUIData):
    """
    Receives a sequence of messages and updates the table
    """
    data.message = receive_message()
    try:
      messages = json.loads(data.message)
    except json.JSONDecodeError:
      print("Error decoding JSON message")
      return
    print(messages, len(messages))
    for message in messages:
      current_values = window[Keys.FILES_PATH].Values
      updated_values = current_values + [[messages[message]]]
      window[Keys.FILES_PATH].update(values=updated_values)
        
    

def remove_files(window, values, data: GUIData):
    files_to_remove = window[Keys.FILES_PATH].get()
    current_files = window[Keys.FILES_PATH].Values
    final_files = [file for [ind, file] in enumerate(current_files) if ind not in files_to_remove]
    window[Keys.FILES_PATH].update(final_files)
  
def receive(window, values, data: GUIData):
  """
    Receives a single message
  """
  data.receiving_message = True
  try: 
    data.message=receive_message()
  except:
    data.message="Error receiving message"
  window[Keys.MESSAGE].update(value=data.message)
  
def save_all(window, values, data: GUIData):
  """
  Saves all messages in the table to a file
  """
  messages = window[Keys.FILES_PATH].Values
  file_path = os.path.join(data.directory_path, values[Keys.FILE_NAME])
  with open(file_path, "w") as file:
    for message in messages:
      file.write(message + ", " + messages[message] + "\n")
  window[Keys.FILES_PATH].update(values=[])