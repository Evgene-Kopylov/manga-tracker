import re
import time
import unittest

from selenium import webdriver
import os

from dotenv import find_dotenv, load_dotenv
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from db.models import Page
from db.session import SessionLocal

load_dotenv(find_dotenv())

os.environ.get("LOCAL_DEV")

session = SessionLocal()


class TestWebListAll(unittest.TestCase):
    def setUp(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        if os.environ.get("LOCAL_DEV"):
            self.url = 'http://127.0.0.1:8000/'
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install())
            )
        else:
            self.driver = webdriver.Remote(
                command_executor='http://localhost:4444',
                options=chrome_options
            )
            self.url = 'insert public addres'  #

    def tearDown(self) -> None:
        self.driver.quit()

    def test_page_delete(self):
        self.driver.get('http://127.0.0.1:8000/add_page/?url=url&element=element&block=block')
        id = re.search(r"\"id\":\d+", self.driver.page_source).group(0)
        id = re.search(r"\d+", id).group(0)
        page = session.query(Page).filter_by(id=id).first()
        assert page
        self.driver.get(self.url)
        print(id)
        time.sleep(0.5)
        delete_btn_id = "remove_page_" + id
        delete_btn = self.driver.find_element(By.ID, delete_btn_id)
        print(delete_btn_id)
        delete_btn.click()
        time.sleep(0.5)
        page = session.query(Page).filter_by(id=id).first()
        assert not page
