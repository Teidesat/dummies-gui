import FreeSimpleGUI as sg
from .progress_data import ProgressData
from requests import post as post_request, get as get_request
from .popup_keys import Keys

BASE_URL = "http://transmitter-server:5000/"

def change_to_next_experiment(window, values, data):
  ENDPOINT = "/next_experiment" 
  get_request(BASE_URL + ENDPOINT)
  update_window(window, data)

def stop_communication():
  ENDPOINT = "/stop_communication" 
  get_request(BASE_URL + ENDPOINT)

def update_window(window: sg.Window, data: ProgressData):
  ENDPOINT = "/current_status"
  response = get_request(BASE_URL + ENDPOINT)
  print(response)
  received_data = response.json()
  print(received_data)
  experiment_id = received_data["experiment_id"]
  experiments = received_data["experiments"]
  messages = received_data["messages"]
  data.set_data(messages, experiments, experiment_id)
  experiment_id_str, messages_str, experiments_str = data.get_formatted(messages, experiments)
  window[Keys.EXP_ID].update(experiment_id_str)
  window[Keys.CURRENT_EXP_PROGRESS].update(current_count=data.total_messages - messages + 1, max=data.total_messages)
  window[Keys.CURRENT_SEQUENCE_PROGRESS].update(current_count=data.total_experiments - experiments + 1, max=data.total_experiments)
  window[Keys.SEQ_PROGRESS_TEXT].update(experiments_str)
  window[Keys.EXP_PROGRESS_TEXT].update(messages_str)