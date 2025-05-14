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

    def test_signup_and_login(self):
        driver = self.driver
        # Go to signup page
        driver.get(self.base_url + "signup")
        # Fill out the signup form
        driver.find_element(By.ID, "first-name").send_keys("Selenium")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        test_email = f"selenium{int(time.time())}@test.com"
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys("TestPassword1!")
        driver.find_element(By.ID, "confirm-password").send_keys("TestPassword1!")
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        # Wait for redirect to inactive page
        time.sleep(1)
        self.assertIn("inactive", driver.current_url)

        # --- Programmatically confirm the user ---
        # Get the confirmation token using the same method as in unit.py
        import sys, os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from app import create_app, db
        from app.models import User
        from app.config import Config  # Use the main config, not TestingConfig
        app = create_app(Config)
        with app.app_context():
            user = User.query.filter_by(email=test_email).first()
            token = user.get_email_verification_token()
        # Visit the confirmation link
        driver.get(self.base_url + f"confirm_email/{token}")
        time.sleep(1)
        self.assertIn("login", driver.current_url)

        # Now log in
        driver.get(self.base_url + "login")
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys("TestPassword1!")
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        time.sleep(1)
        # Should be redirected to add-data page
        self.assertIn("add_data", driver.current_url)

if __name__ == "__main__":
    unittest.main()
