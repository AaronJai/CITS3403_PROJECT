# Unit Testing Guide for EcoTrack

This guide explains how to run the unit tests for the EcoTrack application.

## Prerequisites

- Python 3.6+ installed
- All dependencies installed (`pip install -r requirements.txt`)
- Flask application properly set up

## Running Tests

### From the project root directory:

```bash
# Run all tests
python -m unittest tests/unit.py

# Run tests with verbose output
python -m unittest tests/unit.py -v

# Run all tests in the tests directory
python -m unittest discover tests

# Run a specific test class
python -m unittest tests.unit.UserModelUnitTests
```

### From within the tests folder:

```bash
cd tests
python -m unittest unit.py
```

## Available Test Classes

The unit tests cover the following components:

1. **UserModelUnitTests** 
   - Tests user creation, password hashing, and authentication
   - Tests email verification and password reset token generation

2. **CarbonFootprintModelTests**
   - Tests relationships between the various models
   - Verifies carbon footprint data storage and retrieval

3. **EmissionsCalculationTests**
   - Tests the carbon footprint calculation logic
   - Tests vehicle emissions, travel emissions, and total emissions calculation

4. **ShareModelTests**
   - Tests the sharing functionality between users
   - Verifies share records creation and timestamp generation

## Writing New Tests

To add new tests:

1. Create a new test class that inherits from `BaseTestCase`
2. Write test methods that start with `test_`
3. Use standard unittest assertions like `assertEqual`, `assertTrue`, etc.

Example:

```python
class NewFeatureTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Set up test data
        
    def test_new_feature(self):
        # Test your feature
        self.assertTrue(result)
```
