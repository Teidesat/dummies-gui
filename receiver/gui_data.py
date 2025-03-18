"""
  Simple struct-like class to store the data from the GUI, like the current directory, message, etc
"""

class GUIData:
  def __init__(self, message, directory_path, receiving_message):
    self.message = message
    self.directory_path = directory_path
    self.receiving_message = receiving_message

  # Since assignment cannot be used in lambda functions,
  # setters are necessary to avoid writing a normal function
  # These setters also returns the new value
  def setReceivingMessage(self, value: bool) -> bool:
    self.receiving_message = value
    return value

  def setDirectoryPath(self, value: str) -> str:
    self.directory_path = value
    return value
  
  def setMessage(self, value: str) -> str:
    self.message = value
    return value