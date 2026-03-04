######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Test cases for Pet Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Customer, DataValidationError, db
from .factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Customer   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomer(TestCase):
    """Test Cases for Customer Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_customer(self):
        """It should create a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertIsNotNone(customer.id)
        found = Customer.all()
        self.assertEqual(len(found), 1)
        data = Customer.find(customer.id)
        self.assertEqual(data.name, customer.name)
        self.assertEqual(data.address, customer.address)

    def test_delete_a_customer(self):
        """It should Delete a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)

    def test_list_all_customers(self):
        """It should List all customers in the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        # Create 5 customers
        for _ in range(5):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 customers
        customers = Customer.all()
        self.assertEqual(len(customers), 5)

    def test_find_by_name(self):
        """It should Find a Customer by Name"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        name = customers[0].name
        count = len([customer for customer in customers if customer.name == name])
        found = Customer.find_by_name(name)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.name, name)

    def test_update_a_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertIsNotNone(customer.id)
        customer.name = "John"
        original_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.name, "John")
        found = Customer.find(customer.id)
        self.assertEqual(found.id, original_id)
        self.assertEqual(found.name, "John")

    def test_serialize_a_customer(self):
        """It should Serialize a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertIsNotNone(data)
        self.assertIn("id", data)
        self.assertIn("name", data)
        self.assertIn("address", data)
        self.assertEqual(data["id"], customer.id)
        self.assertEqual(data["name"], customer.name)
        self.assertEqual(data["address"], customer.address)

    def test_deserialize_a_customer(self):
        """It should Deserialize a Customer"""
        data = {
            "name": "Alice",
            "address": "742 Street",
        }
        customer = Customer()
        customer.deserialize(data)
        self.assertEqual(customer.name, "Alice")
        self.assertEqual(customer.address, "742 Street")

    def test_deserialize_missing_name(self):
        """It should not Deserialize a Customer with missing name"""
        data = {"address": "50 Broadway, New York, NY 10004"}
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_missing_address(self):
        """It should not Deserialize a Customer with missing address"""
        data = {"name": "Bob"}
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not Deserialize a Customer with bad data"""
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, "bad data")

    def test_deserialize_none_data(self):
        """It should not Deserialize a Customer with None data"""
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, None)

    def test_find_customer(self):
        """It should Find a Customer by ID"""
        customer = CustomerFactory()
        customer.create()
        found = Customer.find(customer.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, customer.id)
        self.assertEqual(found.name, customer.name)
        self.assertEqual(found.address, customer.address)

    def test_find_customer_not_found(self):
        """It should return None when a Customer is not found"""
        found = Customer.find(0)
        self.assertIsNone(found)

    def test_customer_repr(self):
        """It should return a string representation of a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertIn(customer.name, repr(customer))
        self.assertIn(str(customer.id), repr(customer))

    def test_create_raises_db_error(self):
        """It should raise DataValidationError when the DB raises on create"""
        from unittest.mock import patch

        customer = CustomerFactory()
        with patch(
            "service.models.db.session.commit", side_effect=Exception("DB error")
        ):
            self.assertRaises(DataValidationError, customer.create)

    def test_update_raises_db_error(self):
        """It should raise DataValidationError when the DB raises on update"""
        from unittest.mock import patch

        customer = CustomerFactory()
        customer.create()
        with patch(
            "service.models.db.session.commit", side_effect=Exception("DB error")
        ):
            self.assertRaises(DataValidationError, customer.update)

    def test_delete_raises_db_error(self):
        """It should raise DataValidationError when the DB raises on delete"""
        from unittest.mock import patch

        customer = CustomerFactory()
        customer.create()
        with patch(
            "service.models.db.session.commit", side_effect=Exception("DB error")
        ):
            self.assertRaises(DataValidationError, customer.delete)

    def test_deserialize_attribute_error(self):
        """It should raise DataValidationError when data raises AttributeError on access"""

        class BadData:
            def __getitem__(self, key):
                raise AttributeError("bad attribute")

        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, BadData())
