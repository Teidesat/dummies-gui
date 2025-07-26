#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToDo: Add a description of this module.
"""


class ProgressData:
    """ToDo: Add a description of this class."""

    def __init__(self):
        self.total_messages = None
        self.total_experiments = None
        self.current_experiment = None

    def set_data(self, total_messages, total_experiments, given_experiment: str):
        """ToDo: Add a description of this method."""

        def format_experiment(exp):
            """ToDo: Add a description of this function."""

            message_ind = exp.find("M")
            return exp[0 : message_ind + 1] + "m"

        print(given_experiment)
        given_experiment_formatted = format_experiment(given_experiment)

        if self.current_experiment is None:
            self.total_experiments = total_experiments
            self.total_messages = total_messages
            self.current_experiment = given_experiment_formatted
            return

        if given_experiment_formatted != self.current_experiment:
            self.current_experiment = (given_experiment_formatted,)
            self.total_messages = total_messages

    def get_formatted(self, messages, experiments):
        """ToDo: Add a description of this method."""

        experiment_id_str = str(self.current_experiment)
        num_messages = self.total_messages - messages + 1
        num_experiments = self.total_experiments - experiments + 1
        message_str = f"${num_messages} out of ${self.total_messages}"
        experiment_str = f"${num_experiments} out of ${self.total_experiments}"
        return experiment_id_str, message_str, experiment_str
