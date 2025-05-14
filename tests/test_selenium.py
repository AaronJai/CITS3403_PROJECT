# Selenium UI tests for EcoTrack
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time

class EcoTrackSeleniumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # You can use Chrome, Firefox, or Edge. Make sure the driver is installed and in PATH.
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://127.0.0.1:5000/"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage_loads(self):
        self.driver.get(self.base_url)
        self.assertIn("EcoTrack", self.driver.title)

    def test_login_page_loads(self):
        self.driver.get(self.base_url + "login")
        self.assertIn("Log in", self.driver.title)
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        self.assertIsNotNone(email_input)
        self.assertIsNotNone(password_input)

    # Add more tests for signup, dashboard, etc.

if __name__ == "__main__":
    unittest.main()
