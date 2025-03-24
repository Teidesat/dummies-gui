"""
  Define callbacks to be used in the main loop
"""
import os
import json
import csv
import FreeSimpleGUI as sg

from utils import *
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
    
    for message in messages:
      current_values = window[Keys.EXPERIMENTS].Values
      updated_values = current_values + [[message, messages[message]]]
      window[Keys.EXPERIMENTS].update(values=updated_values)
        
    

def remove_files(window, values, data: GUIData):
    files_to_remove = window[Keys.EXPERIMENTS].get()
    current_files = window[Keys.EXPERIMENTS].Values
    final_files = [file for [ind, file] in enumerate(current_files) if ind not in files_to_remove]
    window[Keys.EXPERIMENTS].update(final_files)
  
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

    table_values = window[Keys.EXPERIMENTS].Values
    print(table_values)
    
    if not table_values:
        sg.popup_error("No data to save!")
        return
    
    file_path = sg.popup_get_file(
        "Save As", 
        save_as=True, 
        default_extension=".csv", 
        file_types=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    
    if not file_path:
        return

    try:
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Message"])
            writer.writerows(table_values)

        sg.popup("File saved successfully!", title="Success")

    except Exception as e:
        sg.popup_error(f"Error saving file: {e}")
