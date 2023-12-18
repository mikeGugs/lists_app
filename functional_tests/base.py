from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException
import os

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        geckodriver_path = ('/snap/bin/geckodriver') # specify geckodriver path
        driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
        self.browser = webdriver.Firefox(options=options, service=driver_service)

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = "http://" + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element('id', 'id_list_table')
                rows = table.find_elements('tag name', 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(.5)

    def get_item_input_box(self):
        return self.browser.find_element('id', 'id_text')
