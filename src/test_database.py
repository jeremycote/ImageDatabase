from SQLManagement import SQLManagement

import pytest

@pytest.mark.parametrize("value, column, strict", [
    ("Cake.jpg", "filename", True),
    ("so", "make", False),
])
def test_SQLManagement_getRowsWithValue_StringTest(value: str, column: str, strict: bool):
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
    sqlManagement = SQLManagement(reload=False)
    
    elements = sqlManagement.getRowsWithValue(value=value, columns=[column], strict=strict)

    willPass = True
    for element in elements:
        if (strict and element[column] != int(value)) or ((not strict) and (int(value) not in element[column])):
            willPass = False

    assert willPass