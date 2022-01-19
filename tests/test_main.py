from typing import Tuple
import pytest
import json

import src.main as main

@pytest.mark.parametrize("value, expected", [
    ("buildings0.jpg", ("buildings1.jpg", "buildings2.jpg", "buildings3.jpg", "buildings4.jpg")),
    ("camper0.jpg", ("camper1.jpg", "camper2.jpg", "camper3.jpg", "camper4.jpg")),
    ("donkey0.jpg", ("donkey1.jpg", "donkey2.jpg", "donkey3.jpg", "donkey4.jpg")),
    ("trees0.jpg", ("trees1.jpg", "trees2.jpg", "trees3.jpg", "trees4.jpg")),
])
def test_FindSimilarTo(value: str, expected: Tuple[str]):
    """
    Test flask image recommendation api.

    Args:
        filename (str): filename of source image.
        expected (List[str]): expected recommendations. Every element must be recommended to pass.
    """

    response = main.find_similar_to(value, 60, 10)
    recommendations = json.loads(response[0])

    matches = 0

    for recommendation in recommendations:
        if recommendation["filename"] in expected:
            matches += 1

    assert matches == len(expected)

# @pytest.mark.parametrize("value", [
#     ("buildings0.jpg"),
# ])
# def test_FindSimilarTo_FileNotFound(value: str):
#     result = app.get("/api/similar_to/" + value + "/70/10")

#     assert result.data == value + " is not in database"