import pytest
import requests


class TestAny:
    """
    playground
    """

    def test_get(self):
        response = requests.get(url="http://localhost:8000/")
        print(response.content.decode('utf-8'))

    def test_1(self):
        response = requests.post(
            url="http://localhost:8000/add",
            data='a1'
        )
        print(response.content.decode('utf-8'))
