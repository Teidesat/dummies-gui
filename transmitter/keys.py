"""The keys used for the events or layout elements in the GUI"""

import enum

class Keys(enum.Enum):
  EXIT = "-EXIT-"
  STOP = "-STOP-"
  SEND = "-SEND-"
  EXP_ID = "-EXP-ID-"
  LOAD_SETTINGS = "-LOAD_SETTINGS-"
  SAVE_SETTINGS = "-SAVE_SETTINGS-"
  DIR_PATH = "-DIR_PATH-"
  FILES_LIST = "-FILES_LIST-"
  FILES_PATH = "-FILES_PATH-"
  MESSAGE = "-MESSAGE-"
  # Visibility related keys
  TOGGLE_PLAIN_TEXT = "-TOGGLE_SEC-PLAIN_TEXT-"
  TOGGLE_FILE = "-TOGGLE_SEC-FILE-"
  TOGGLE_EXP = "-TOGGLE_SEC-EXP-"
  TOGGLE_SEQ = "-TOGGLE_SEC-SEQ-"
  # Section related keys
  SEC_FILE = "-SEC-FILE-"
  SEC_PLAIN_TEXT = "-SEC-PLAIN_TEXT-"
  SEC_EXP = "-SEC-EXP-"
  SEC_SEQ = "-SEC-SEQ-"
