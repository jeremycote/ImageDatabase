from cmath import exp
import os

from src.SQLManagement import SQLManagement, formatDateTime
from src.constants import PATH_IMAGES_RAW, PATH_DB

import pytest

def test_SQLManagement_getAllRows():
    """
    SQLManagement creates database using all images in PATH_IMAGES_RAW.
    Thus, getAllRows should return a list with the same length as the number of images in PATH_IMAGES_RAW.
    """
    sqlManagement = SQLManagement(reload=True)

    nImages = len(os.listdir(PATH_IMAGES_RAW))

    rows = sqlManagement.getAllRows()

    assert len(rows) == nImages



@pytest.mark.parametrize("value, column, strict", [
    ("Cake.jpg", "filename", True),
    ("so", "make", False),
])
def test_SQLManagement_getRowsWithValue_StringTest(value: str, column: str, strict: bool):
    """
    Test that all rows returned actually contain value.
    If strict, columns must contain exact value. Else, column contains value as substring.

    Args:
        value (str): value to search in database.
        column (str): column to search in database.
        strict (bool): should do strict search.
    """
    sqlManagement = SQLManagement(reload=False)
    
    elements = sqlManagement.getRowsWithValue(value=value, columns=[column], strict=strict)

    willPass = True
    for element in elements:
        if (strict and (element[column].lower() != value.lower())) or ((not strict) and (value.lower() not in element[column].lower())):
            willPass = False

    assert willPass


@pytest.mark.parametrize("value, column, strict", [
    ("1", "id", True),
])
def test_SQLManagement_getRowsWithValue_IntegerTest(value: str, column: str, strict: bool):
    """
    Test that all rows returned actually contain value.
    If strict, columns must contain exact value. Else, column contains value as substring.

    Matches are casted to int to verify that they are truly integers.

    Args:
        value (str): value to search in database.
        column (str): column to search in database.
        strict (bool): should do strict search.
    """
    sqlManagement = SQLManagement(reload=False)
    
    elements = sqlManagement.getRowsWithValue(value=value, columns=[column], strict=strict)

    willPass = True
    for element in elements:
        if (strict and element[column] != int(value)) or ((not strict) and (int(value) not in element[column])):
            willPass = False

    assert willPass

@pytest.mark.parametrize("value, expected", [
    ("10-10-10 10:10:10", "10-10-10 10:10:10"),
    ("10:10:10 10:10:10", "10-10-10 10:10:10"),
    ("10-10-10 10-10-10", "10-10-10 10:10:10"),
    ("19:20-40 10:10:1", "19-20-40 10:10:1")
])
def test_SQLManagement_formatDateTime(value: str, expected: str):
    """
    Test that EXIF datetime is translated into python compatible datetime format.

    Args:
        value (str): datetime string to convert.
        expected (str): datetime string result.
    """

    result = formatDateTime(value)
    assert result == expected