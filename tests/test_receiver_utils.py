import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock

sys.path.append(str(Path(__file__).resolve().parents[1]/"receiver"))

import utils as utils
from utils import parse_id, binary_to_ascii, ascii_to_binary
from dotenv import load_dotenv

def test_parse_id():
    exp_id = "CO_D3.0-A0.0-I0.5-F30.0-L1.0-Mm"
    result = utils.parse_id("CO_D3.0-A0.0-I0.5-F30.0-L1.0-Mm")

    assert result["distance"] == "3.0"
    assert result["angle"] == "0.0"
    assert result["intensity"] == "0.5"
    assert result["frequency"] == "30.0"
    assert result["batch"] == "1.0"

def test_parse_id_invalid():
    with pytest.raises(ValueError):
        utils.parse_id("invalid_id")

def test_binary_to_ascii():
    result = utils.binary_to_ascii("010010000110010101101100011011000110111100100000011101110110111101110010011011000110010000100001")
    assert result == "Hello world!"

def test_ascii_to_binary():
    result = utils.ascii_to_binary("Hello world!")
    assert result == "010010000110010101101100011011000110111100100000011101110110111101110010011011000110010000100001"


def test_assert_directory(tmp_path):
    # Test with a valid directory
    utils.assert_directory(tmp_path)

    # Test with an invalid directory
    with pytest.raises(NotADirectoryError):
        utils.assert_directory(tmp_path / "non_existent_directory") 