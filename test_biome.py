"""
    test_biome
    ~~~~~~~~~~
"""
import os
import pathlib

import biome
import pytest


def str2bool(string):
    """Convert a string to bool.

    Args:
        string (str): Must be 'true' or 'false', case insensitive.

    Raises:
        ValueError: If the string cannot be parsed as bool
    """
    lower = string.lower()
    if lower not in ("true", "false"):
        raise ValueError("cannot interpret %r as boolean")
    return lower == "true"


def setup_module(module):
    """Setup test environment."""
    os.environ["YOURAPP_HOST"] = "dev.yourapp"
    os.environ["YOURAPP_PORT"] = "5000"
    os.environ["YOURAPP_BOOL_TITLE"] = "True"
    os.environ["YOURAPP_BOOL_LOWER"] = "false"
    os.environ["YOURAPP_BOOL_UPPER"] = "TRUE"
    os.environ["YOURAPP_PATH"] = str(pathlib.Path("foo") / "bar")


def test_access_case_sensitivity():
    expected_host = os.environ["YOURAPP_HOST"]
    assert (biome.YOURAPP.HOST == expected_host and
            biome.YOURAPP.host == expected_host and
            biome.yourapp.HOST == expected_host and
            biome.yourapp.host == expected_host)


def test_access_defaults():
    assert biome.YOURAPP.get("host", "default") != "default"
    assert biome.YOURAPP.get("driver", "sqlite") == "sqlite"
    assert biome.YOURAPP.get_bool("production", False) is False
    assert biome.YOURAPP.get_int("throttle_seconds", 60) == 60
    assert biome.YOURAPP.get_path("config", "dev.conf") == "dev.conf"


def test_access_missing():
    for getter in ("get", "get_bool", "get_int", "get_path"):
        with pytest.raises(KeyError) as excinfo:
            getattr(biome.YOURAPP, getter)("foo")
        assert "EnvironmentError" in str(excinfo)


def test_access_trailing_underscore():
    assert biome.YOURAPP == biome.YOURAPP_


def test_explicit_access_literals():
    assert biome.YOURAPP.get("host") == biome.YOURAPP["host"]

    assert biome.YOURAPP.get_int("port") == int(os.environ["YOURAPP_PORT"])

    # Title case boolean ('True' or 'False')
    bool_title = os.environ["YOURAPP_BOOL_TITLE"]
    assert biome.YOURAPP.get_bool("bool_title") == str2bool(bool_title)

    # Lower case boolean ('true' or 'false')
    bool_lower = os.environ["YOURAPP_BOOL_LOWER"]
    assert biome.YOURAPP.get_bool("bool_lower") == str2bool(bool_lower)

    # Upper case boolean ('TRUE' or 'FALSE')
    bool_upper = os.environ["YOURAPP_BOOL_UPPER"]
    assert biome.YOURAPP.get_bool("bool_upper") == str2bool(bool_upper)

    # Integer values should be interpretable as bool, as expected
    assert biome.YOURAPP.get_bool("port") == bool(biome.YOURAPP.PORT)

    with pytest.raises(ValueError):
        assert biome.YOURAPP.get_bool("host")

    assert biome.YOURAPP.get_path("path") == \
        pathlib.Path(os.environ["YOURAPP_PATH"])


def test_implicit_access_literals():
    assert biome.YOURAPP.port == int(os.environ["YOURAPP_PORT"])

    bool_title = os.environ["YOURAPP_BOOL_TITLE"]
    assert biome.YOURAPP.bool_title == str2bool(bool_title)

    bool_lower = os.environ["YOURAPP_BOOL_LOWER"]
    assert biome.YOURAPP.bool_lower == str2bool(bool_lower)

    assert biome.YOURAPP.path == pathlib.Path(os.environ["YOURAPP_PATH"])


def test_refresh():
    os.environ["YOURAPP_DEBUG"] = "True"
    assert "debug" not in biome.YOURAPP
    biome.YOURAPP.refresh()
    assert "debug" in biome.YOURAPP