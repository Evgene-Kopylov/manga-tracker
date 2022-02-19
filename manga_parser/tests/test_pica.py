import unittest

from insta_ckeck import InstaMangaParser


class TestConnect(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = InstaMangaParser()

    def test_connect(self):
        """
        Требуется доступ к серверу брокера
        """
        channel = self.parser.connect()
        assert channel.is_open
