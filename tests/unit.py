import unittest
import os
from app import create_app, db
from app.config import TestingConfig
from app.models import User, CarbonFootprint, Travel, Vehicle, Home, Food, Shopping, Emissions, Share
from app.processing_layer import CarbonFootprintCalculator


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
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
        
    def test_user_creation(self):
        user = User(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            confirmed=True
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        queried_user = User.query.filter_by(email='john@example.com').first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.first_name, 'John')
        self.assertEqual(queried_user.last_name, 'Doe')
        self.assertTrue(queried_user.confirmed)
        
    def test_email_verification_token(self):
        user = User(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com'
        )
        user.set_password('secret')
        db.session.add(user)
        db.session.commit()
        
        token = user.get_email_verification_token()
        self.assertIsNotNone(token)
        
        verified_user = User.verify_email_token(token)
        self.assertEqual(verified_user.id, user.id)
        
        # Test invalid token
        invalid_token = "invalid.token.string"
        self.assertIsNone(User.verify_email_token(invalid_token))
    
    def test_password_reset_token(self):
        user = User(
            first_name='Alex',
            last_name='Brown',
            email='alex@example.com'
        )
        user.set_password('oldpassword')
        db.session.add(user)
        db.session.commit()
        
        token = user.get_reset_password_token()
        self.assertIsNotNone(token)
        
        verified_user = User.verify_reset_password_token(token)
        self.assertEqual(verified_user.id, user.id)
        
        # Test password change
        verified_user.set_password('newpassword')
        db.session.commit()
        
        self.assertFalse(user.check_password('oldpassword'))
        self.assertTrue(user.check_password('newpassword'))


class CarbonFootprintModelTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a test user
        self.user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            confirmed=True
        )
        self.user.set_password('testpass')
        db.session.add(self.user)
        db.session.commit()
        
        # Create test data objects
        self.travel = Travel(
            public_transit_distance=500,
            air_travel_distance=1000,
            bus_kms=200,
            transit_rail_kms=150,
            short_flights=1,
            medium_flights=1
        )
        
        self.vehicle = Vehicle(
            fuel_type='gasoline',
            distance=10000,
            fuel_efficiency=8.5
        )
        
        self.home = Home(
            electricity=500,
            electricity_unit='kWh',
            electricity_frequency='/mo',
            clean_energy_percentage=20.0,
            natural_gas=50,
            natural_gas_unit='m³',
            natural_gas_frequency='/mo',
            living_space=150.0,
            water_usage=200.0
        )
        
        self.food = Food(
            meat_fish_eggs=0.3,
            grains_baked_goods=0.5,
            dairy=0.4,
            fruits_vegetables=0.7,
            snacks_drinks=0.2
        )
        
        self.shopping = Shopping(
            goods_multiplier=1.2,
            services_multiplier=0.8
        )
        
        db.session.add_all([self.travel, self.home, self.food, self.shopping])
        db.session.commit()
        
        # Assign vehicle to travel
        self.vehicle.travel_id = self.travel.id
        db.session.add(self.vehicle)
        db.session.commit()
        
        # Create a carbon footprint record
        self.carbon_footprint = CarbonFootprint(
            user_id=self.user.id,
            travel_id=self.travel.id,
            home_id=self.home.id,
            food_id=self.food.id,
            shopping_id=self.shopping.id
        )
        db.session.add(self.carbon_footprint)
        db.session.commit()
    
    def test_carbon_footprint_relationships(self):
        # Check that relationships are set up correctly
        footprint = CarbonFootprint.query.first()
        self.assertEqual(footprint.user_id, self.user.id)
        self.assertEqual(footprint.travel_id, self.travel.id)
        self.assertEqual(footprint.home_id, self.home.id)
        self.assertEqual(footprint.food_id, self.food.id)
        self.assertEqual(footprint.shopping_id, self.shopping.id)
        
        # Test relationship navigation
        self.assertEqual(footprint.travel.public_transit_distance, 500)
        self.assertEqual(footprint.home.electricity, 500)
        self.assertEqual(footprint.food.meat_fish_eggs, 0.3)
        self.assertEqual(footprint.shopping.goods_multiplier, 1.2)


class EmissionsCalculationTests(BaseTestCase):
    """
    Tests for calculating carbon emissions using the CarbonFootprintCalculator.
    
    USAGE: 
    To run just this test class from the root directory:
    python -m unittest tests.unit.EmissionsCalculationTests
    """
    def setUp(self):
        super().setUp()
        # Create test user
        self.user = User(
            first_name='Carbon',
            last_name='Tester',
            email='carbon@example.com',
            confirmed=True
        )
        self.user.set_password('testpass')
        db.session.add(self.user)
        db.session.commit()
        
    def test_vehicle_emissions_calculation(self):
        # Create emissions object and calculator
        emissions = Emissions(user_id=self.user.id)
        calculator = CarbonFootprintCalculator(emissions)
        
        # Create test vehicles
        vehicles = [
            Vehicle(
                travel_id=1,  # Mock ID
                fuel_type='gasoline',
                distance=10000,
                fuel_efficiency=8.0
            ),
            Vehicle(
                travel_id=1,  # Mock ID
                fuel_type='diesel',
                distance=5000,
                fuel_efficiency=6.0
            )
        ]
        
        # Calculate emissions
        car_emissions = calculator.calculate_vehicles(vehicles)
        
        # Check that emissions were calculated and assigned to the emissions object
        self.assertIsNotNone(car_emissions)
        self.assertGreater(car_emissions, 0.0)
        self.assertEqual(car_emissions, emissions.car_emissions)
    
    def test_travel_emissions_calculation(self):
        # Create emissions object and calculator
        emissions = Emissions(user_id=self.user.id)
        calculator = CarbonFootprintCalculator(emissions)
        
        # Create test travel data
        travel = Travel(
            public_transit_distance=0,
            air_travel_distance=0,
            bus_kms=200,
            transit_rail_kms=100,
            commuter_rail_kms=50,
            intercity_rail_kms=300,
            short_flights=2,
            medium_flights=1,
            long_flights=1,
            extended_flights=0
        )
        
        # Calculate emissions with advanced mode
        travel_emissions = calculator.calculate_travel('advanced', travel)
        
        # Check that public transit and air travel emissions were calculated
        self.assertIsNotNone(travel_emissions['public_transit'])
        self.assertIsNotNone(travel_emissions['air_travel'])
        self.assertGreater(travel_emissions['public_transit'], 0.0)
        self.assertGreater(travel_emissions['air_travel'], 0.0)
        
        # Check that emissions were assigned to the emissions object
        self.assertEqual(travel_emissions['public_transit'], emissions.public_transit_emissions)
        self.assertEqual(travel_emissions['air_travel'], emissions.air_travel_emissions)
    
    def test_total_emissions_calculation(self):
        # Create emissions object with known values
        emissions = Emissions(
            user_id=self.user.id,
            car_emissions=2.5,
            public_transit_emissions=0.8,
            air_travel_emissions=3.2,
            electricity_emissions=1.5,
            natural_gas_emissions=1.2,
            heating_fuels_emissions=0.5,
            water_emissions=0.3,
            construction_emissions=0.4,
            meat_emissions=2.1,
            dairy_emissions=0.7,
            fruits_vegetables_emissions=0.3,
            cereals_emissions=0.4,
            snacks_emissions=0.6,
            clothing_emissions=0.9,
            furniture_emissions=0.3,
            other_goods_emissions=0.8,
            services_emissions=0.9
        )
        
        calculator = CarbonFootprintCalculator(emissions)
        
        # Calculate total emissions
        total = calculator.calculate_total_emissions()
        
        # Expected total is the sum of all emissions values
        expected_total = sum([
            emissions.car_emissions,
            emissions.public_transit_emissions,
            emissions.air_travel_emissions,
            emissions.electricity_emissions,
            emissions.natural_gas_emissions,
            emissions.heating_fuels_emissions,
            emissions.water_emissions,
            emissions.construction_emissions,
            emissions.meat_emissions,
            emissions.dairy_emissions,
            emissions.fruits_vegetables_emissions,
            emissions.cereals_emissions,
            emissions.snacks_emissions,
            emissions.clothing_emissions,
            emissions.furniture_emissions,
            emissions.other_goods_emissions,
            emissions.services_emissions
        ])
        
        # Check calculated total against expected total
        self.assertEqual(total, expected_total)
        self.assertEqual(emissions.total_emissions, expected_total)


class ShareModelTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create test users
        self.user1 = User(
            first_name='User',
            last_name='One',
            email='user1@example.com',
            confirmed=True
        )
        self.user1.set_password('password1')
        
        self.user2 = User(
            first_name='User',
            last_name='Two',
            email='user2@example.com',
            confirmed=True
        )
        self.user2.set_password('password2')
        
        db.session.add_all([self.user1, self.user2])
        db.session.commit()
    
    def test_share_creation(self):
        # Create a share record
        share = Share(
            from_user_id=self.user1.id,
            to_user_id=self.user2.id
        )
        db.session.add(share)
        db.session.commit()
        
        # Verify share was created
        shares = Share.query.all()
        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0].from_user_id, self.user1.id)
        self.assertEqual(shares[0].to_user_id, self.user2.id)
        
        # Test share record has timestamp
        self.assertIsNotNone(shares[0].shared_date)


if __name__ == '__main__':
    unittest.main()
