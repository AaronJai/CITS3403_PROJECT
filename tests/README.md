# Unit & Selenium Testing Guide for EcoTrack

This guide explains how to run the unit and Selenium UI tests for the EcoTrack application.

## Prerequisites

- Python 3.6+ installed
- All dependencies installed (`pip install -r requirements.txt`)
- Flask application properly set up and running (for Selenium tests)
- ChromeDriver (or another WebDriver) installed and in your PATH for Selenium

## Running Tests

### From the project root directory:

**UNIT TESTS**
```bash
# Run all unit tests
python -m unittest tests/unit.py

# Run tests with verbose output
python -m unittest tests/unit.py -v

# Run all tests in the tests directory
python -m unittest discover tests

# Run a specific test class e.g.,
python -m unittest tests.unit.UserModelUnitTests
```

**SELENIUM UI TESTS**
```bash
# Make sure your Flask server is running (e.g. flask run or python EcoTrack.py)

# Run all Selenium UI tests
python -m unittest tests.test_selenium

# Or, using the module runner (both work, but unittest is preferred for test discovery)
python -m tests.test_selenium

# Run Selenium tests with verbose output
python -m unittest tests.test_selenium -v

# Run specific selenium tests e.g.,
python -m unittest tests.test_selenium.EcoTrackSeleniumTests.test_07_delete_user
```

**Note:**
- Always run Selenium tests from the project root, not from inside the tests folder.
- If you get import errors, use the `python -m unittest ...` form from the project root.

### From within the tests folder (unit tests only):

```bash
cd tests
python -m unittest unit.py
```

## Available Test Classes

### Unit Tests (`unit.py`)

1. **UserModelUnitTests**
   - Tests user creation, password hashing, and authentication
   - Tests email verification and password reset token generation/validation
   - Tests password change logic

2. **CarbonFootprintModelTests**
   - Tests relationships between User, CarbonFootprint, Travel, Home, Food, Shopping, Vehicle
   - Verifies correct data storage and relationship navigation

3. **EmissionsCalculationTests**
   - Tests the carbon footprint calculation logic
   - Tests vehicle emissions, travel emissions (advanced mode), and total emissions calculation

4. **ShareModelTests**
   - Tests the sharing functionality between users
   - Verifies share records creation and timestamp generation

5. **MessageModelTests**
   - Tests sending and receiving messages between users
   - Verifies message content, sender/receiver, and timestamp

### Selenium UI Tests (`test_selenium.py`)

- **EcoTrackSeleniumTests**
  - `test_01_homepage_loads`: Homepage loads and title is correct
  - `test_02_auth_pages`: Login and signup pages load, all fields are present
  - `test_03_signup_and_login`: Full signup, email confirmation, and login flow
  - `test_04_add_data_simple`: Add data using the simple mode, stepper navigation, and calculation
  - `test_05_add_data_advanced`: Add data using advanced mode, including all advanced fields
  - `test_06_change_details`: Change name, email, and password from the profile page, and verify changes
  - `test_07_delete_user`: Delete account from profile, verify user cannot log in again

## Writing New Tests

To add new tests:

1. Create a new test class that inherits from `BaseTestCase` (for unit tests) or `unittest.TestCase` (for Selenium tests)
2. Write test methods that start with `test_`
3. Use standard unittest assertions like `assertEqual`, `assertTrue`, etc.

Example (unit test):
```python
class NewFeatureTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Set up test data
    def test_new_feature(self):
        # Test your feature
        self.assertTrue(result)
```

Example (Selenium test):
```python
def test_dashboard_loads(self):
    self.driver.get(self.base_url + "dashboard")
    self.assertIn("Dashboard", self.driver.title)
```

## Troubleshooting
- If you get `ModuleNotFoundError: No module named 'app'`, make sure you are running tests from the project root and using the `python -m unittest ...` form.
- If Selenium cannot find elements, check your form field IDs and selectors in the templates.
- If you get database errors in Selenium tests, ensure your Flask server is running and using the same database as your test code for direct DB access.
