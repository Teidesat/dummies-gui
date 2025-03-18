"""The keys used for the events or layout elements in the GUI"""

import enum

class Keys(enum.Enum):
  EXIT_1 = "-EXIT-1-"
  EXIT_2 = "-EXIT-2-"
  MESSAGE = "-MESSAGE-"
  RECEIVE = "-RECEIVE-"
  STOP = "-STOP-"
  CLEAN = "-CLEAN-"
  DIR_NAME = "-DIR_NAME-"
  FILE_NAME = "-FILE_NAME-"
  PATH_ERROR_MSG = "-PATH-ERROR-MSG-"
  SAVE = "-SAVE-"
  # Visibility related keys
  TOGGLE_SEC_SAVE_FILE = "-TOGGLE_SEC-SAVE_FILE-"
  TOGGLE_SEC_SHOW_TEXT = "-TOGGLE_SEC-SHOW_TEXT-"
  # Section related keys
  SEC_SHOW_TEXT = "-SEC-SHOW_TEXT-"
  SEC_SAVE_FILE =  "-SEC-SAVE_FILE-"

VISIBILITY_KEYS = [
  Keys.TOGGLE_SEC_SAVE_FILE,
  Keys.TOGGLE_SEC_SHOW_TEXT
]

EXIT_KEYS = [
  Keys.EXIT_1,
  Keys.EXIT_2
]