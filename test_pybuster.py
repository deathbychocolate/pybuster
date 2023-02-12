import pytest
import pybuster as pb
import constants


@pytest.mark.count_lines
def test_count_lines_should_count_0_lines_in_file():
    error_message = """
    Number of lines do not equal 0.
    """
    assert pb._count_lines_in_file(constants.FILEPATH_TEST_FILES_0_LINE_FILE) == 0, error_message


@pytest.mark.count_lines
def test_count_lines_should_count_1_lines_in_file():
    error_message = """
    Number of lines do not equal 1.
    """
    assert pb._count_lines_in_file(constants.FILEPATH_TEST_FILES_1_LINE_FILE) == 1, error_message


@pytest.mark.count_lines
def test_count_lines_should_count_10_lines_in_file():
    error_message = """
    Number of lines do not equal 10.
    """
    assert pb._count_lines_in_file(constants.FILEPATH_TEST_FILES_10_LINE_FILE) == 10, error_message


@pytest.mark.count_lines
def test_count_lines_should_count_100_lines_in_file():
    error_message = """
    Number of lines do not equal 100.
    """
    assert (
        pb._count_lines_in_file(constants.FILEPATH_TEST_FILES_100_LINE_FILE) == 100
    ), error_message


@pytest.mark.index_file
def test_should_raise_a_value_error_when_the_filepath_is_an_empty_file():
    with pytest.raises(ValueError):
        pb._index_the_file(constants.FILEPATH_TEST_FILES_0_LINE_FILE).values()


# @pytest.mark.index_file
# @pytest.mark.index_file
# @pytest.mark.index_file
