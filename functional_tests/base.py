from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException
import os
from .server_tools import reset_database

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
            reset_database(self.staging_server)

    def tearDown(self):
        self.browser.quit()

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(.5)
        return modified_fn

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element('id', 'id_list_table')
        rows = table.find_elements('tag name', 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn):
        return fn
    
    def get_item_input_box(self):
        return self.browser.find_element('id', 'id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element('link text', 'Log out')
        navbar = self.browser.find_element('css selector', '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        lambda: self.browser.find_element('name', 'email')
        navbar = self.browser.find_element('css selector', '.navbar')
        self.assertNotIn(email, navbar.text)
