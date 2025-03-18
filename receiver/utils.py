"""
  Various utility functions used throughout the program
"""

from requests import get as get_request

def receive_message():
    """Function to receive the message from the transmitter server."""

    # ToDo: Change request address and endpoint to receive the message from the receiver
    #  dummy's server instead of the transmitter server, it's currently the same server
    #  to test the communication between the two dummies GUIs.
    response = get_request("http://transmitter-server:5000/get_message_data")

    if response.status_code != 200:
        raise ConnectionError(
            f"Failed to receive message from server with error code {response.status_code}."
        )

    return response.text