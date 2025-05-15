# Selenium UI tests for EcoTrack
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time
import threading
from werkzeug.serving import make_server

class EcoTrackSeleniumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start Flask app server in a background thread
        import sys, os
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        # Optionally, also silence Flask's own logger
        logging.getLogger('flask.app').setLevel(logging.ERROR)
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from app import create_app, db
        from app.models import User
        from app.config import Config
        cls.app = create_app(Config)
        cls.db = db
        cls.User = User
        cls.base_url = "http://127.0.0.1:5000/"

        class ServerThread(threading.Thread):
            def __init__(self, app):
                threading.Thread.__init__(self)
                self.srv = make_server('127.0.0.1', 5000, app)
                self.ctx = app.app_context()
                self.ctx.push()
                self.daemon = True
            def run(self):
                self.srv.serve_forever()
            def shutdown(self):
                self.srv.shutdown()

        cls.server_thread = ServerThread(cls.app)
        cls.server_thread.start()
        time.sleep(0.5)  # Give server time to start

        # Selenium driver
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server_thread.shutdown()

    def setUp(self):
        self.driver.delete_all_cookies()
        # Optionally, ensure logged out
        self.driver.get(self.base_url + "logout")

    def signup_confirm_login(self, email, password):
        driver = self.driver
        driver.get(self.base_url + "signup")
        driver.find_element(By.ID, "first-name").send_keys("Selenium")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "confirm-password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        time.sleep(1)
        self.assertIn("inactive", driver.current_url)
        with self.app.app_context():
            user = self.User.query.filter_by(email=email).first()
            token = user.get_email_verification_token()
        driver.get(self.base_url + f"confirm_email/{token}")
        time.sleep(1)
        self.assertIn("login", driver.current_url)
        driver.get(self.base_url + "login")
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        time.sleep(1)
        self.assertIn("add_data", driver.current_url)

    def test_01_homepage_loads(self):
        self.driver.get(self.base_url)
        self.assertIn("EcoTrack", self.driver.title)

    def test_02_auth_pages(self):
        driver = self.driver
        # Test login page loads and fields are present
        driver.get(self.base_url + "login")
        self.assertIn("Log in", driver.title)
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        self.assertIsNotNone(email_input)
        self.assertIsNotNone(password_input)
        # Click the sign up link/button on the login form
        signup_link = driver.find_element(By.LINK_TEXT, "Sign Up")
        signup_link.click()
        time.sleep(0.5)
        # Now on the signup page, check fields
        self.assertIn("Sign Up", driver.title)
        first_name = driver.find_element(By.ID, "first-name")
        last_name = driver.find_element(By.ID, "last-name")
        email = driver.find_element(By.ID, "email")
        password = driver.find_element(By.ID, "password")
        confirm_password = driver.find_element(By.ID, "confirm-password")
        self.assertIsNotNone(first_name)
        self.assertIsNotNone(last_name)
        self.assertIsNotNone(email)
        self.assertIsNotNone(password)
        self.assertIsNotNone(confirm_password)

    def test_03_signup_and_login(self):
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)

    def test_04_add_data_simple(self):
        driver = self.driver
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        # Step through each section using the stepper's Next button
        for _ in range(3):  # There are 4 steps, so click Next 3 times
            next_btn = driver.find_element(By.CSS_SELECTOR, '[data-stepper-next-btn]')
            next_btn.click()
            time.sleep(0.5)
        # Now the Calculate Footprint button should be visible
        finish_btn = driver.find_element(By.CSS_SELECTOR, '[data-stepper-finish-btn]')
        driver.execute_script("arguments[0].classList.remove('hidden');", finish_btn)  # Ensure it's visible
        finish_btn.click()
        time.sleep(2)
        self.assertIn("view_data", driver.current_url)

    def test_05_add_data_advanced(self):
        driver = self.driver
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        # --- Step 1: Travel (select Advanced, fill all advanced inputs) ---
        driver.find_element(By.ID, "show-advanced").click()
        # Wait for vehicle-distance input to appear
        for _ in range(20):
            try:
                vehicle_distance_input = driver.find_element(By.ID, "vehicle-distance")
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise Exception("vehicle-distance input not found after waiting")
        vehicle_distance_input.clear()
        vehicle_distance_input.send_keys("15000")
        # Fill advanced public transit fields
        adv_ids = [
            'public_transit_advanced-bus_kms',
            'public_transit_advanced-transit_rail_kms',
            'public_transit_advanced-commuter_rail_kms',
            'public_transit_advanced-intercity_rail_kms',
        ]
        adv_vals = ["100", "200", "300", "400"]
        for adv_id, val in zip(adv_ids, adv_vals):
            el = driver.find_element(By.ID, adv_id)
            el.clear()
            el.send_keys(val)
        # Fill advanced air travel fields
        air_ids = [
            'air_travel_advanced-short_flights',
            'air_travel_advanced-medium_flights',
            'air_travel_advanced-long_flights',
            'air_travel_advanced-extended_flights',
        ]
        air_vals = ["2", "3", "1", "0"]
        for air_id, val in zip(air_ids, air_vals):
            el = driver.find_element(By.ID, air_id)
            el.clear()
            el.send_keys(val)
        driver.find_element(By.CSS_SELECTOR, '[data-stepper-next-btn]').click()
        time.sleep(0.5)

        # --- Step 2: Home (fill all number/range inputs) ---
        driver.find_element(By.ID, "electricity").clear()
        driver.find_element(By.ID, "electricity").send_keys("1200")
        driver.find_element(By.ID, "natural-gas").clear()
        driver.find_element(By.ID, "natural-gas").send_keys("500")
        driver.find_element(By.ID, "heating-oil").clear()
        driver.find_element(By.ID, "heating-oil").send_keys("250")
        driver.find_element(By.ID, "living-space").clear()
        driver.find_element(By.ID, "living-space").send_keys("100")
        # Sliders for clean energy and water usage
        clean_slider = driver.find_element(By.CSS_SELECTOR, '[name="home_energy-clean_energy_percentage"]')
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", clean_slider, "40")
        water_slider = driver.find_element(By.CSS_SELECTOR, '[name="home_energy-water_usage"]')
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", water_slider, "120")
        driver.find_element(By.CSS_SELECTOR, '[data-stepper-next-btn]').click()
        time.sleep(0.5)

        # --- Step 3: Food (fill all sliders) ---
        food_ids = [
            'food-meat_fish_eggs',
            'food-grains_baked_goods',
            'food-dairy',
            'food-fruits_vegetables',
            'food-snacks_drinks',
        ]
        for food_id in food_ids:
            slider = driver.find_element(By.CSS_SELECTOR, f'[name="{food_id}"]')
            driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", slider, "2.0")
        driver.find_element(By.CSS_SELECTOR, '[data-stepper-next-btn]').click()
        time.sleep(0.5)

        # --- Step 4: Shopping (select Advanced, fill all advanced inputs) ---
        driver.find_element(By.ID, "show-advanced-shopping").click()
        time.sleep(0.3)
        shopping_ids = [
            'input_input_footprint_shopping_goods_furnitureappliances',
            'input_input_footprint_shopping_goods_clothing',
            'input_input_footprint_shopping_goods_entertainment',
            'input_input_footprint_shopping_goods_officesupplies',
            'input_input_footprint_shopping_goods_personalcare',
            'input_input_footprint_shopping_services_food',
            'input_input_footprint_shopping_services_education',
            'input_input_footprint_shopping_services_communication',
            'input_input_footprint_shopping_services_loan',
            'input_input_footprint_shopping_services_transport',
        ]
        shopping_vals = ["100", "200", "50", "30", "40", "60", "70", "80", "90", "110"]
        for shop_id, val in zip(shopping_ids, shopping_vals):
            el = driver.find_element(By.ID, shop_id)
            el.clear()
            el.send_keys(val)
        driver.find_element(By.CSS_SELECTOR, '[data-stepper-finish-btn]').click()
        time.sleep(2)
        self.assertIn("view_data", driver.current_url)

    def test_06_change_details(self):
        driver = self.driver
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        # Go to profile page
        driver.get(self.base_url + "profile")
        # Change name
        first_name_input = driver.find_element(By.NAME, "first_name")
        last_name_input = driver.find_element(By.NAME, "last_name")
        first_name_input.clear()
        first_name_input.send_keys("NewFirst")
        last_name_input.clear()
        last_name_input.send_keys("NewLast")
        driver.find_element(By.NAME, "submit_name").click()
        time.sleep(1)
        driver.refresh()
        # Check that the updated name appears in the profile header
        header = driver.find_element(By.CSS_SELECTOR, "h1.text-3xl.font-bold.pt-4")
        self.assertIn("NewFirst NewLast", header.text)
        # Change email
        new_email = f"selenium_new{int(time.time())}@test.com"
        email_input = driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(new_email)
        driver.find_element(By.NAME, "submit_email").click()
        time.sleep(1)
        # Confirm new email via token
        with self.app.app_context():
            user = self.User.query.filter_by(email=test_email).first()
            self.assertIsNotNone(user)
            self.assertEqual(user.unconfirmed_email, new_email)
            token = user.get_email_update_token(new_email)
        driver.get(self.base_url + f"confirm_new_email/{token}")
        time.sleep(1)
        # Go to profile page again (user is still logged in)
        driver.get(self.base_url + "profile")
        # Change password
        driver.find_element(By.NAME, "current_password").send_keys(password)
        new_password = "TestPassword2!"
        driver.find_element(By.NAME, "new_password").send_keys(new_password)
        driver.find_element(By.NAME, "confirm_password").send_keys(new_password)
        driver.find_element(By.NAME, "submit").click()
        time.sleep(1)
        # Log out using the Logout button (find by text and href)
        logout_btn = driver.find_element(By.XPATH, "//a[contains(@href, '/logout') and .//span[text()='Logout']]")
        logout_btn.click()
        time.sleep(0.5)
        # Log in with new email and new password
        driver.get(self.base_url + "login")
        driver.find_element(By.ID, "email").send_keys(new_email)
        driver.find_element(By.ID, "password").send_keys(new_password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        time.sleep(1)
        self.assertIn("add_data", driver.current_url)
    
    def test_07_delete_user(self):
        driver = self.driver
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        # Go to profile page
        driver.get(self.base_url + "profile")
        # Click delete account button and handle prompt
        delete_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Delete Account')]")
        driver.execute_script("arguments[0].click();", delete_btn)
        time.sleep(0.5)
        # Handle JS prompt for confirmation
        alert = driver.switch_to.alert
        alert.send_keys("DELETE")
        alert.accept()
        # Wait for redirect to login page
        time.sleep(3)
        self.assertIn("login", driver.current_url)
        # Try to log in again (should fail)
        driver.get(self.base_url + "login")
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        time.sleep(1)
        # Should remain on login page or see error
        self.assertIn("login", driver.current_url)
        # Optionally, check for error message
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue("Invalid email or password" in body_text or "login" in driver.current_url)

if __name__ == "__main__":
    unittest.main()
