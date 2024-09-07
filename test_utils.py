import pytest

# Import the function you want to test
from docker_version_dashboard.project.app.convert_time import convertTime

# Test cases


@pytest.mark.disabled
def test_convertTime_minutes_only():
    assert convertTime("0:30") == 30


@pytest.mark.disabled
def test_convertTime_hours_and_minutes():
    assert convertTime("1:45") == 105


def test_convertTime_hours_minutes_and_seconds():
    assert convertTime("2:30:15") == 150.25


def test_convertTime_zero_time():
    assert convertTime("0:0:0") == 0


@pytest.mark.disabled
def test_convertTime_invalid_time_format():
    with pytest.raises(ValueError):
        convertTime("1:45:60")


@pytest.mark.disabled
def test_convertTime_negative_time():
    with pytest.raises(ValueError):
        convertTime("-1:30")


def test_convertTime_invalid_separator():
    with pytest.raises(ValueError):
        convertTime("3-30")


def test_convertTime_string_instead_of_int():
    with pytest.raises(ValueError):
        convertTime("2:30:A")
