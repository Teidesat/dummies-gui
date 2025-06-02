#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple struct-like class to store the data from the GUI, like the current directory,
message, etc.
"""


class GUIData:
    # ToDo: Add docstrings to the class and its methods

    def __init__(self, message, directory_path, receiving_message):
        self.message = message
        self.directory_path = directory_path
        self.receiving_message = receiving_message

    # Since assignment cannot be used in lambda functions,
    # setters are necessary to avoid writing a normal function
    # These setters also returns the new value
    def set_receiving_message(self, value: bool) -> bool:
        self.receiving_message = value
        return value

    def set_directory_path(self, value: str) -> str:
        self.directory_path = value
        return value

    def set_message(self, value: str) -> str:
        self.message = value
        return value
