# from typing import Tuple
# import pytest

# from src.main import app, PATH_STATIC

# @pytest.mark.parametrize("value, expected", [
#     ("buildings0.jpg", ("buildings1.jpg, buildings2.jpg, buildings3.jpg, buildings4.jpg")),
# ])
# def test_FindSimilarTo(value: str, expected: Tuple[str]):
#     recommendations = app.get("/api/similar_to/" + value + "/70/10")
#     print(recommendations)
#     matches = 0
#     for recommendation in recommendations:
#         if recommendation["filename"] in expected:
#             matches += 1

#     assert matches == len(expected)

# @pytest.mark.parametrize("value", [
#     ("buildings0.jpg"),
# ])
# def test_FindSimilarTo_FileNotFound(value: str):
#     result = app.get("/api/similar_to/" + value + "/70/10")

#     assert result.data == value + " is not in database"