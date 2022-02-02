from datetime import datetime
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
            self.url_add_page = 'http://127.0.0.1:8000/add_page/?url=url&element=element&block=block'
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install())
            )
        else:
            self.driver = webdriver.Remote(
                command_executor='http://localhost:4444',
                options=chrome_options
            )
            self.url = ''  # ipublic addres

    def tearDown(self) -> None:
        self.driver.quit()

    def test_page_delete(self):
        self.driver.get(self.url_add_page)
        id = re.search(r"\"id\":\d+", self.driver.page_source).group(0)
        id = re.search(r"\d+", id).group(0)
        page = session.query(Page).filter_by(id=id).first()
        assert page
        self.driver.get(self.url)
        print(id)
        time.sleep(0.6)
        delete_btn_id = "remove_page_" + id
        delete_btn = self.driver.find_element(By.ID, delete_btn_id)
        print(delete_btn_id)
        delete_btn.click()
        time.sleep(0.3)
        page = session.query(Page).filter_by(id=id).first()
        assert not page

    def test_edit_page_name(self):
        self.driver.get(self.url_add_page)
        id = re.search(r"\"id\":\d+", self.driver.page_source).group(0)
        id = re.search(r"\d+", id).group(0)
        time.sleep(0.1)
        self.driver.get(self.url)
        time.sleep(0.6)
        safe_click = self.driver.find_element(By.ID, 'safe_click')
        edit_page_id = 'edit_page_' + id
        edit_btn = self.driver.find_element(By.ID, edit_page_id)
        edit_btn.click()
        name_field_id = 'name_field_' + id
        name_field = self.driver.find_element(By.ID, name_field_id)
        name_field.clear()
        safe_click.click()
        time.sleep(0.1)
        new_name = ''.join([x for x in str(datetime.now()) if x.isdigit()])
        edit_btn.click()
        name_field = self.driver.find_element(By.ID, name_field_id)
        name_field.send_keys(new_name)
        time.sleep(0.1)
        safe_click.click()
        time.sleep(0.2)
        page = session.query(Page).filter_by(id=id).first()
        assert page.name == new_name

    def test_page_new(self):
        self.driver.get(self.url_add_page)
        _id = re.search(r"\"id\":\d+", self.driver.page_source).group(0)
        page_id = re.search(r"\d+", _id).group(0)
        time.sleep(0.1)

        page = session.query(Page).filter_by(id=page_id).first()
        page.chapters = '1, 2, 3, 4, 5'
        page.new = 2
        session.commit()
        self.driver.get(self.url)
        time.sleep(0.6)
        new_id = 'new_' + page_id
        new_el = self.driver.find_element(By.ID, new_id)
        print(new_el.text)
        new_num = new_el.text[2:-1]
        print(new_num)

        page.new = 3
        session.commit()
        new_el.click()
        time.sleep(0.5)
        new_el = self.driver.find_element(By.ID, new_id)
        assert new_el.text == '(+3)'
