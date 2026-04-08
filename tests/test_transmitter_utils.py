import tempfile

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock

sys.path.append(str(Path(__file__).resolve().parents[1]/"transmitter"))

import utils as utils
from utils import get_current_experiment_id, send_message, str_to_binary_str
from dotenv import load_dotenv

def test_get_current_experiment_id():
    settings = {
        "dummy_distance": 3.0,
        "transmitter_angle": 0.0,
        "led_intensity": 0.5,
        "blinking_frequency": 30.0,
        "messages_batch": 1.0,
    }
    result = get_current_experiment_id(settings)
    assert result == "CO_D3.0-A0.0-I0.5-F30.0-L1.0-Mm"

@patch("utils.post_request")
def test_send_message_raises_for_non_200(post_mock):
    post_mock.return_value = Mock(status_code=500)
    utils.TRANSMITTER_SERVER_BASE_URL = "http://testserver"

    settings = {
        "dummy_distance": 3.0,
        "transmitter_angle": 0.0,
        "led_intensity": 0.5,
        "blinking_frequency": 30.0,
        "messages_batch": 1.0,
    }

    with pytest.raises(ConnectionError):


        utils.send_message("hola", settings)

@patch("utils.post_request")
def test_send_message(post_mock):
    post_mock.return_value = Mock(status_code=200)
    utils.TRANSMITTER_SERVER_BASE_URL = "http://testserver"
    settings = {
        "dummy_distance": 3.0,
        "transmitter_angle": 0.0,
        "led_intensity": 0.5,
        "blinking_frequency": 30.0,
        "messages_batch": 1.0,
    }
    utils.send_message("hola", settings)

def test_str_to_binary_str():
    result = utils.str_to_binary_str("Hi")
    assert result == "0100100001101001"

def test_get_files_from_path():
    # Create a temporary directory with some files
    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = Path(temp_dir) / "file1.txt"
        file2 = Path(temp_dir) / "file2.txt"
        file1.touch()
        file2.touch()

        # Test that the function returns the correct files
        result = utils.get_files_from_path(temp_dir)
        assert set(result) == {str(file1), str(file2)}

        # Test that the function raises an error for an invalid path
        with pytest.raises(NotADirectoryError):
            utils.get_files_from_path(str(Path(temp_dir) / "non_existent_directory")) 

@patch("utils.post_request")
def test_send_message_conection_timeout(post_mock):
    post_mock.side_effect = ConnectionError("Connection timed out")
    utils.TRANSMITTER_SERVER_BASE_URL = "http://testserver"
    settings = {
        "dummy_distance": 3.0,
        "transmitter_angle": 0.0,
        "led_intensity": 0.5,
        "blinking_frequency": 30.0,
        "messages_batch": 1.0,
    }
    with pytest.raises(ConnectionError):
        utils.send_message("hola", settings)
        