# import pytest
import unittest

import json

from fastapi.testclient import TestClient
from main import app


class TestAddTitle(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_api(self):
        response = self.client.get("/add_title?url=a&element=b&block=c")
        assert json.loads(response.content.decode('utf-8')) \
               == {"url": "a", "element": "b", "block": "c"}
