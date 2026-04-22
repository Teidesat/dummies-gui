#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple struct-like class to store the data from the GUI, like the current directory,
message, etc.
"""

from typing import Optional


class GUIData:
    # ToDo: Add docstrings to the class and its methods

    def __init__(self, message, directory_path, receiving_message):
        self.message = message
        self.directory_path = directory_path
        self.receiving_message = receiving_message
        self.recording_enabled = False
        self.record_file_path = None
        self.record_file = None
        self.record_start_time = 0.0

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

    def start_recording(self, file_path: str) -> str:
        self.record_file_path = file_path
        self.record_file = open(file_path, "a", encoding="utf-8")
        self.recording_enabled = True
        return file_path

    def stop_recording(self) -> Optional[str]:
        last_file_path = self.record_file_path
        self.recording_enabled = False

        if self.record_file is not None:
            self.record_file.close()

        self.record_file = None
        self.record_file_path = None
        self.record_start_time = 0.0
        return last_file_path

    def append_record(self, text: str) -> None:
        if not self.recording_enabled or self.record_file is None:
            return

        self.record_file.write(text + "\n")
        self.record_file.flush()
