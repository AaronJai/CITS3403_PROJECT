# Selenium UI tests for EcoTrack
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        import io
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        # Optionally, also silence Flask's own logger
        logging.getLogger('flask.app').setLevel(logging.ERROR)
        # Redirect stdout/stderr to suppress server print output during tests
        cls._original_stdout = sys.stdout
        cls._original_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from app import create_app, db
        from app.models import User
        from app.config import TestingConfig
        cls.app = create_app(TestingConfig)
        cls.db = db
        cls.User = User
        cls.base_url = "http://127.0.0.1:3000/"

        # Drop and recreate all tables for a clean test DB
        with cls.app.app_context():
            cls.db.drop_all()
            cls.db.create_all()

        class ServerThread(threading.Thread):
            def __init__(self, app):
                threading.Thread.__init__(self)
                self.srv = make_server('127.0.0.1', 3000, app)
                self.ctx = app.app_context()
                self.ctx.push()
                self.daemon = True
            def run(self):
                self.srv.serve_forever()
            def shutdown(self):
                self.srv.shutdown()

        cls.server_thread = ServerThread(cls.app)
        cls.server_thread.start()

        # Poll the server until it's ready instead of fixed sleep
        import requests
        for _ in range(40):  # Try for up to 10 seconds (40 x 0.25s)
            try:
                r = requests.get(cls.base_url)
                if r.status_code == 200:
                    break
            except Exception:
                pass
            time.sleep(0.25)
        else:
            raise RuntimeError("Flask server did not start in time")

        # Selenium driver
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server_thread.shutdown()
        # Restore stdout/stderr
        import sys
        sys.stdout = cls._original_stdout
        sys.stderr = cls._original_stderr
        # Drop all tables after tests
        with cls.app.app_context():
            cls.db.drop_all()

    def setUp(self):
        self.driver.delete_all_cookies()
        # Optionally, ensure logged out
        self.driver.get(self.base_url + "logout")
        # Clean DB before each test for isolation
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
            self.db.create_all()

    def signup_confirm_login(self, email, password):
        driver = self.driver
        wait = self.wait
        driver.get(self.base_url + "signup")
        wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        driver.find_element(By.ID, "first-name").send_keys("Selenium")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "confirm-password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        wait.until(EC.url_contains("inactive"))
        with self.app.app_context():
            user = self.User.query.filter_by(email=email).first()
            token = user.get_email_verification_token()
        driver.get(self.base_url + f"confirm_email/{token}")
        wait.until(EC.url_contains("login"))
        driver.get(self.base_url + "login")
        wait.until(EC.presence_of_element_located((By.ID, "email")))
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        wait.until(EC.url_contains("add_data"))

    def test_01_homepage_loads(self):
        self.driver.get(self.base_url)
        self.wait.until(EC.title_contains("EcoTrack"))
        self.assertIn("EcoTrack", self.driver.title)

    def test_02_auth_pages(self):
        driver = self.driver
        wait = self.wait
        driver.get(self.base_url + "login")
        wait.until(EC.presence_of_element_located((By.ID, "email")))
        self.assertIn("Log in", driver.title)
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        self.assertIsNotNone(email_input)
        self.assertIsNotNone(password_input)
        signup_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up")))
        signup_link.click()
        wait.until(EC.title_contains("Sign Up"))
        self.assertIn("Sign Up", driver.title)
        wait.until(EC.presence_of_element_located((By.ID, "first-name")))
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
        wait = self.wait
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        for _ in range(3):
            next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stepper-next-btn]')))
            next_btn.click()
            wait.until(lambda d: next_btn.is_enabled())
        finish_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stepper-finish-btn]')))
        driver.execute_script("arguments[0].classList.remove('hidden');", finish_btn)
        finish_btn.click()
        wait.until(EC.url_contains("view_data"))

    def test_05_add_data_advanced(self):
        driver = self.driver
        wait = self.wait
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        driver.find_element(By.ID, "show-advanced").click()
        vehicle_distance_input = wait.until(EC.presence_of_element_located((By.ID, "vehicle-distance")))
        vehicle_distance_input.clear()
        vehicle_distance_input.send_keys("15000")
        adv_ids = [
            'public_transit_advanced-bus_kms',
            'public_transit_advanced-transit_rail_kms',
            'public_transit_advanced-commuter_rail_kms',
            'public_transit_advanced-intercity_rail_kms',
        ]
        adv_vals = ["100", "200", "300", "400"]
        for adv_id, val in zip(adv_ids, adv_vals):
            el = wait.until(EC.presence_of_element_located((By.ID, adv_id)))
            el.clear()
            el.send_keys(val)
        air_ids = [
            'air_travel_advanced-short_flights',
            'air_travel_advanced-medium_flights',
            'air_travel_advanced-long_flights',
            'air_travel_advanced-extended_flights',
        ]
        air_vals = ["2", "3", "1", "0"]
        for air_id, val in zip(air_ids, air_vals):
            el = wait.until(EC.presence_of_element_located((By.ID, air_id)))
            el.clear()
            el.send_keys(val)
        next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stepper-next-btn]')))
        driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        next_btn.click()
        wait.until(EC.presence_of_element_located((By.ID, "electricity")))
        driver.find_element(By.ID, "electricity").clear()
        driver.find_element(By.ID, "electricity").send_keys("1200")
        driver.find_element(By.ID, "natural-gas").clear()
        driver.find_element(By.ID, "natural-gas").send_keys("500")
        driver.find_element(By.ID, "heating-oil").clear()
        driver.find_element(By.ID, "heating-oil").send_keys("250")
        driver.find_element(By.ID, "living-space").clear()
        driver.find_element(By.ID, "living-space").send_keys("100")
        clean_slider = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[name="home_energy-clean_energy_percentage"]')))
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", clean_slider, "40")
        water_slider = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[name="home_energy-water_usage"]')))
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", water_slider, "120")
        next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stepper-next-btn]')))
        driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        next_btn.click()
        food_ids = [
            'food-meat_fish_eggs',
            'food-grains_baked_goods',
            'food-dairy',
            'food-fruits_vegetables',
            'food-snacks_drinks',
        ]
        for food_id in food_ids:
            slider = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'[name="{food_id}"]')))
            driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", slider, "2.0")
        next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stepper-next-btn]')))
        driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        next_btn.click()
        driver.find_element(By.ID, "show-advanced-shopping").click()
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
            el = wait.until(EC.presence_of_element_located((By.ID, shop_id)))
            el.clear()
            el.send_keys(val)
        finish_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stepper-finish-btn]')))
        driver.execute_script("arguments[0].scrollIntoView();", finish_btn)
        finish_btn.click()
        wait.until(EC.url_contains("view_data"))

    def test_06_change_details(self):
        driver = self.driver
        wait = self.wait
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        driver.get(self.base_url + "profile")
        first_name_input = wait.until(EC.presence_of_element_located((By.NAME, "first_name")))
        last_name_input = wait.until(EC.presence_of_element_located((By.NAME, "last_name")))
        first_name_input.clear()
        first_name_input.send_keys("NewFirst")
        last_name_input.clear()
        last_name_input.send_keys("NewLast")
        driver.find_element(By.NAME, "submit_name").click()
        wait.until(EC.staleness_of(first_name_input))
        driver.refresh()
        header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-3xl.font-bold.pt-4")))
        self.assertIn("NewFirst NewLast", header.text)
        new_email = f"selenium_new{int(time.time())}@test.com"
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_input.clear()
        email_input.send_keys(new_email)
        driver.find_element(By.NAME, "submit_email").click()
        wait.until(EC.presence_of_element_located((By.NAME, "email")))
        with self.app.app_context():
            user = self.User.query.filter_by(email=test_email).first()
            token = user.get_email_update_token(new_email)
        driver.get(self.base_url + f"confirm_new_email/{token}")
        wait.until(EC.url_contains("profile"))
        driver.get(self.base_url + "profile")
        driver.find_element(By.NAME, "current_password").send_keys(password)
        new_password = "TestPassword2!"
        driver.find_element(By.NAME, "new_password").send_keys(new_password)
        driver.find_element(By.NAME, "confirm_password").send_keys(new_password)
        driver.find_element(By.NAME, "submit").click()
        wait.until(EC.url_contains("profile"))
        logout_btn = wait.until(EC.element_to_be_clickable((By.ID, "logout-btn")))
        logout_btn.click()
        wait.until(EC.url_contains("login"))
        driver.get(self.base_url + "login")
        wait.until(EC.presence_of_element_located((By.ID, "email")))
        driver.find_element(By.ID, "email").send_keys(new_email)
        driver.find_element(By.ID, "password").send_keys(new_password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        wait.until(EC.url_contains("add_data"))

    def test_07_delete_user(self):
        driver = self.driver
        wait = self.wait
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        driver.get(self.base_url + "profile")
        delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Delete Account')]")))
        driver.execute_script("arguments[0].click();", delete_btn)
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.send_keys("DELETE")
        alert.accept()
        wait.until(EC.url_contains("login"))
        driver.get(self.base_url + "login")
        wait.until(EC.presence_of_element_located((By.ID, "email")))
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        # if we stay on login, the account was deleted
        wait.until(EC.url_contains("login"))

    def test_08_facts_page(self):
        driver = self.driver
        wait = self.wait
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        driver.get(self.base_url + "facts")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#news-feed .zoom")))
        self.assertIn("About EcoTrack", driver.page_source)
        self.assertIn("Latest Environmental News", driver.page_source)
        news_items = driver.find_elements(By.CSS_SELECTOR, "#news-feed .zoom")
        self.assertGreaterEqual(len(news_items), 1)
        first_news = news_items[0]
        news_links = first_news.find_elements(By.CSS_SELECTOR, "a.text-xl.font-bold")
        self.assertTrue(news_links[1].get_attribute("href").startswith("http"))
        self.assertTrue(len(news_links[1].text.strip()) > 0)

    def test_09_dashboard_page(self):
        driver = self.driver
        wait = self.wait
        test_email = f"selenium{int(time.time())}@test.com"
        password = "TestPassword1!"
        self.signup_confirm_login(test_email, password)
        for _ in range(3):
            next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stepper-next-btn]')))
            next_btn.click()
            wait.until(lambda d: next_btn.is_enabled())
        finish_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-stepper-finish-btn]')))
        driver.execute_script("arguments[0].classList.remove('hidden');", finish_btn)
        finish_btn.click()
        wait.until(EC.url_contains("view_data"))
        driver.get(self.base_url)
        wait.until(EC.presence_of_element_located((By.ID, "emission-goal-card")))
        emission_goal = driver.find_element(By.ID, "emission-goal-card")
        emission_goal.click()
        wait.until(EC.url_contains("view_data"))
        self.assertIn("view_data", driver.current_url)
        driver.back()
        wait.until(EC.presence_of_element_located((By.ID, "emission-goal-card")))
        categories = ["travel", "home", "food", "shopping"]
        for idx, cat in enumerate(categories):
            card = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f".category-card[data-category='{cat}']")))
            card.click()
            wait.until(EC.url_contains("view_data"))
            self.assertIn("view_data", driver.current_url)
            self.assertIn(f"tab={idx}", driver.current_url)
            self.assertIn("#emissions-summary", driver.current_url)
            driver.back()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f".category-card[data-category='{cat}']")))

    def test_10_share_page(self):
        driver = self.driver
        wait = self.wait
        # --- User 1 signup and logout ---
        user1_email = f"selenium_msg1_{int(time.time())}@test.com"
        user1_password = "TestPassword1!"
        self.signup_confirm_login(user1_email, user1_password)
        driver.get(self.base_url + "profile")
        logout_btn = wait.until(EC.element_to_be_clickable((By.ID, "logout-btn")))
        logout_btn.click()
        wait.until(EC.url_contains("login"))

        # --- User 2 signup ---
        user2_email = f"selenium_msg2_{int(time.time())}@test.com"
        user2_password = "TestPassword1!"
        self.signup_confirm_login(user2_email, user2_password)
        driver.get(self.base_url + "share")
        # Search for user1 by email
        search_box = wait.until(EC.presence_of_element_located((By.ID, "search-email")))
        search_box.clear()
        search_box.send_keys(user1_email)
        # Wait for the "Share" submit button and click it
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form .button-primary[type='submit']"))).click()
        share_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), 'Share with')]")))
        share_btn.click()
        # Now user1 should appear in 'People You're Sharing With'
        # Find and click the dropdown button to reveal the shared users list
        dropdown_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.text-gray-400")))
        dropdown_btn.click()
        chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), 'Chat')]")))
        chat_btn.click()
        # Wait for chat box
        wait.until(EC.visibility_of_element_located((By.ID, "chatBox")))
        chat_input = wait.until(EC.presence_of_element_located((By.ID, "chatInput")))
        chat_input.send_keys("Hello from user2!")
        chat_form = driver.find_element(By.ID, "chatForm")
        chat_form.submit()
        # Wait for message to appear
        wait.until(lambda d: "Hello from user2!" in d.find_element(By.ID, "chatMessages").text)
        # Logout user2
        driver.get(self.base_url + "profile")
        logout_btn = wait.until(EC.element_to_be_clickable((By.ID, "logout-btn")))
        logout_btn.click()
        wait.until(EC.url_contains("login"))

        # --- User 1 logs back in, shares with user2, and checks chat ---
        driver.get(self.base_url + "login")
        wait.until(EC.presence_of_element_located((By.ID, "email")))
        driver.find_element(By.ID, "email").send_keys(user1_email)
        driver.find_element(By.ID, "password").send_keys(user1_password)
        driver.find_element(By.CSS_SELECTOR, "form input[type='submit']").click()
        wait.until(EC.url_contains("add_data"))
        driver.get(self.base_url + "share")
        # Search for user2 by email
        search_box = wait.until(EC.presence_of_element_located((By.ID, "search-email")))
        search_box.clear()
        search_box.send_keys(user2_email)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form .button-primary[type='submit']"))).click()
        share_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), 'Share with')]")))
        share_btn.click()
        # Now user1 should appear in 'People You're Sharing With'
        # Find and click the dropdown button to reveal the shared users list
        dropdown_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.text-gray-400")))
        dropdown_btn.click()
        # Now user2 should appear in 'People You're Sharing With'
        chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), 'Chat')]")))
        chat_btn.click()
        wait.until(EC.visibility_of_element_located((By.ID, "chatBox")))
        # Assert the message from user2 is visible
        wait.until(lambda d: "Hello from user2!" in d.find_element(By.ID, "chatMessages").text)
        self.assertIn("Hello from user2!", driver.find_element(By.ID, "chatMessages").text)
    
if __name__ == "__main__":
    unittest.main()
