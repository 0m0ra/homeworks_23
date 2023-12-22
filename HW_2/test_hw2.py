"""Test module for Clients statistics module."""

import os

import pytest

from hw2 import process_data

SUCCESSFUL_TESTS = (
    ('tests/test.json', 'output.json', 'tests/output_test.json'),
    ('tests/test.json', 'dir1/dir2/output.json', 'tests/output_test.json'),
)

ERROR_TESTS = (
    ('tests/error_test.json', ValueError),
    ('tests/empty_test.json', ValueError),
    ('tests/empty_file.json', ValueError),
    ('undefined.json', ValueError),
)


@pytest.mark.parametrize('input_file, output_file, expected_file', SUCCESSFUL_TESTS)
def test_module(
    input_file: str,
    output_file: str,
    expected_file: str,
) -> None:
    """Test process_data function from hw2.py.

    Args:
        input_file (str): path to input json file.
        output_file (str): path to output json file.
        expected_file (str): path to answers json file.
    """
    process_data(input_file, output_file)
    assert os.path.exists(output_file)
    with open(output_file) as output_data:
        checking_data = output_data.read()
    with open(expected_file) as expected_data:
        answers = expected_data.read()
    assert checking_data == answers
    os.remove(output_file)


@pytest.mark.parametrize('input_file, error', ERROR_TESTS)
def test_errors(
    input_file: str,
    error: type,
) -> None:
    """Test for error handling from process_data function.

    Args:
        input_file (str): path to input json file.
        error (type): the error that should be caused.
    """
    with pytest.raises(error):
        process_data(input_file, 'some_file.json')
