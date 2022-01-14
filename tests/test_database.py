from numpy import fabs
from entities.ImageEntity import ImageEntity
from database.SQLManagement import SQLManagement

import pytest

@pytest.mark.parametrize("filename", [("Cake.jpg"), ("R1.jpg"), ("R2.jpg")])
def test_SQLManagement_getElementsWithFilename(filename: str):
    sqlManagement = SQLManagement(reload=False)
    
    elements = sqlManagement.getElementsWithFilename(filename)

    willPass = True
    for element in elements:
        if element.filename != filename:
            willPass = False

    assert willPass