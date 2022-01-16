from typing import List
import pytest
from src.Img2VecResnet18 import Img2VecResnet18

recognizer = Img2VecResnet18(reload=True)

@pytest.mark.parametrize("filename, expected", [
    ("Cake.jpg", ["Cake copy.jpg"]),
    ("buildings0.jpg", ["buildings1.jpg", "buildings2.jpg", "buildings3.jpg", "buildings4.jpg", "buildings5.jpg"]),
    ("trees0.jpg", ["trees1.jpg", "trees2.jpg", "trees3.jpg", "trees4.jpg"]),
    ("rio0.jpg", ["rio1.jpg", "rio2.jpg", "rio3.jpg", "rio4.jpg"]),
    ("GizaEgypt.jpg", ["pyramiden0.jpg", "pyramiden1.jpg", "pyramiden2.jpg", "pyramiden3.jpg", "pyramiden4.jpg"])
])
def test_Img2VecResnet18_getSimilarImages(filename: str, expected: List[str]):
    """
    Test that recommended images are similar to source.

    Args:
        filename (str): filename of source image.
        expected (List[str]): expected recommendations. Every element must be recommended to pass.

    """

    print(expected)

    simImages, simValues = recognizer.getSimilarImages(filename)

    count = 0

    for image in simImages:
        if image in expected:
            print(image)
            count += 1
    
    assert count == len(expected)