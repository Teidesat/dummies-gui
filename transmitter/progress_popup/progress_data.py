#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class to handle and format the progress data for the GUI popup.
"""

class ProgressData:
    def __init__(self):
        self.total_messages = None
        self.total_experiments = None
        self.current_experiment = None
        self.is_finished = False

    def set_data(self, total_messages, total_experiments, given_experiment: str):
        # 1. Si el servidor nos dice que no hay nada ("None"), ignoramos la actualización
        if given_experiment == "None" or given_experiment is None:
            self.is_finished = True
            return

        def format_experiment(exp):
            message_ind = exp.find("M")
            if message_ind == -1: 
                return exp  # Seguridad por si no encuentra la M
            return exp[0 : message_ind + 1] + "m"

        given_experiment_formatted = format_experiment(given_experiment)

        if self.current_experiment is None:
            self.total_experiments = total_experiments
            self.total_messages = total_messages
            self.current_experiment = given_experiment_formatted
            return

        if given_experiment_formatted != self.current_experiment:
            # 2. Corregido el bug de la coma traicionera que creaba una tupla
            self.current_experiment = given_experiment_formatted
            self.total_messages = total_messages

    def get_formatted(self, messages, experiments):
        # 3. Si ya no quedan experimentos ni mensajes, ¡hemos terminado!
        if experiments == 0 and messages == 0:
            self.is_finished = True
            return "Finished", "All messages sent!", "Sequence complete!"

        experiment_id_str = str(self.current_experiment)
        
        # 4. Limitamos la matemática para que nunca pase del máximo (evita el 5 de 4)
        num_messages = min(self.total_messages - messages + 1, self.total_messages)
        num_experiments = min(self.total_experiments - experiments + 1, self.total_experiments)
        
        message_str = f"${num_messages} out of ${self.total_messages}"
        experiment_str = f"${num_experiments} out of ${self.total_experiments}"
        
        return experiment_id_str, message_str, experiment_str

