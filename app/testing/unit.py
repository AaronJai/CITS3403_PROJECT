import unittest
from app import create_app, db
from app.config import TestingConfig
from app.models import User, CarbonFootprint, Travel, Vehicle, Home, Food, Shopping, Emissions, Share

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        testApp = create_app(TestingConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class UserModelUnitTests(BaseTestCase):
    def test_password_hashing(self):
        user = User(first_name='Emily', email='test@student.uwa.edu.au')
        user.set_password('ecotrack')
        self.assertFalse(user.check_password('ecotrack789'))
        self.assertTrue(user.check_password('ecotrack'))