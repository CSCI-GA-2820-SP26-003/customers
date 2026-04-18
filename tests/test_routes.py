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
TestCustomer API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Customer
from tests.factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/customers"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertIn("name", data)
        self.assertIn("version", data)
        self.assertIn("paths", data)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    def test_ui(self):
        """It should render the customer administration UI page"""
        response = self.client.get("/ui")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Customer Administration", response.get_data(as_text=True))

    def test_create_customer(self):
        """It should Create a new Customer"""
        test_customer = CustomerFactory()
        logging.debug("Test Customer: %s", test_customer.serialize())
        response = self.client.post(
            "/customers",
            json=test_customer.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_customer = response.get_json()
        self.assertEqual(new_customer["name"], test_customer.name)
        self.assertEqual(new_customer["address"], test_customer.address)
        self.assertIsNotNone(new_customer["id"])

    def test_create_customer_missing_name(self):
        """It should not Create a Customer with missing name"""
        test_customer = CustomerFactory()
        customer_data = test_customer.serialize()
        del customer_data["name"]
        logging.debug("Test Customer without name: %s", customer_data)
        response = self.client.post(
            "/customers", json=customer_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("name", data["message"])

    def test_create_customer_missing_address(self):
        """It should not Create a Customer with missing address"""
        test_customer = CustomerFactory()
        customer_data = test_customer.serialize()
        del customer_data["address"]
        logging.debug("Test Customer without address: %s", customer_data)
        response = self.client.post(
            "/customers", json=customer_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("address", data["message"])

    def test_create_customer_empty_name(self):
        """It should not Create a Customer with an empty name"""
        test_customer = CustomerFactory()
        customer_data = test_customer.serialize()
        customer_data["name"] = ""
        logging.debug("Test Customer with empty name: %s", customer_data)
        response = self.client.post(
            "/customers", json=customer_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("required", data["message"])

    def test_create_customer_empty_address(self):
        """It should not Create a Customer with an empty address"""
        test_customer = CustomerFactory()
        customer_data = test_customer.serialize()
        customer_data["address"] = ""
        logging.debug("Test Customer with empty address: %s", customer_data)
        response = self.client.post(
            "/customers", json=customer_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("required", data["message"])

    def test_create_customer_no_content_type(self):
        """It should not Create a Customer with no Content-Type"""
        test_customer = CustomerFactory()
        response = self.client.post("/customers", data=test_customer.serialize())
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_customer_wrong_content_type(self):
        """It should not Create a Customer with wrong Content-Type"""
        test_customer = CustomerFactory()
        response = self.client.post(
            "/customers", json=test_customer.serialize(), content_type="text/plain"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_get_customer(self):
        """It should retrieve a customers details"""
        # test_customer = self._create_customer(1)[0]
        test_customer = CustomerFactory()
        test_customer.create()
        # response = self.client.post(BASE_URL, json=self.test_get_customer.serialize())
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_customer.name)

    def test_get_customer_not_found(self):
        """It should not Get a Customer thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_get_customer_list(self):
        """It should Get a list of customers"""
        # self._create_customer(5)
        customers = CustomerFactory.create_batch(5)
        for customer in customers:
            customer.create()
        response = self.client.get(BASE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_update_customer(self):
        """It should Update a Customer"""
        test_customer = CustomerFactory()
        test_customer.create()
        self.assertEqual(len(Customer.all()), 1)

        updated_data = {"name": "Updated Name", "address": "Updated Address"}
        response = self.client.put(
            f"{BASE_URL}/{test_customer.id}",
            json=updated_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], updated_data["name"])
        self.assertEqual(data["address"], updated_data["address"])

    def test_delete_customer(self):
        """It should Delete a Customer"""
        test_customer = CustomerFactory()
        test_customer.create()
        self.assertEqual(len(Customer.all()), 1)

        response = self.client.delete(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Customer.all()), 0)

    def test_delete_customer_not_found(self):
        """It should return 204 even when deleting a Customer that does not exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_customer_not_found(self):
        """It should return 404 when updating a Customer that does not exist"""
        updated_data = {"name": "Ghost", "address": "Nowhere"}
        response = self.client.put(
            f"{BASE_URL}/0",
            json=updated_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    def test_method_not_allowed(self):
        """It should return 405 for a method that is not allowed"""
        # PATCH is not defined on /customers
        response = self.client.patch(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_query_customers_by_name(self):
        """It should return only customers matching the queried name"""
        customers = CustomerFactory.create_batch(5)
        for customer in customers:
            customer.create()
        target_name = customers[0].name
        customers[1].name = target_name
        customers[1].update()

        response = self.client.get(BASE_URL, query_string={"name": target_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        for customer in data:
            self.assertEqual(customer["name"], target_name)

    def test_query_customers_by_name_no_match(self):
        """It should return an empty list when no customers match the queried name"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()

        response = self.client.get(
            BASE_URL, query_string={"name": "NonExistentName12345"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data, [])

    def test_list_customers_without_query(self):
        """It should return all customers when no query string is provided"""
        customers = CustomerFactory.create_batch(4)
        for customer in customers:
            customer.create()

        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 4)

    def test_suspend_a_customer(self):
        """It should Suspend an existing Customer"""
        test_customer = CustomerFactory()
        test_customer.create()

        response = self.client.put(f"{BASE_URL}/{test_customer.id}/suspend")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "suspended")

    def test_suspend_nonexistent_customer(self):
        """It should return 404 when suspending a Customer that does not exist"""
        response = self.client.put(f"{BASE_URL}/0/suspend")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    def test_suspended_status_persists(self):
        """It should persist the suspended status after a GET"""
        test_customer = CustomerFactory()
        test_customer.create()

        self.client.put(f"{BASE_URL}/{test_customer.id}/suspend")

        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "suspended")

    def test_activate_a_customer(self):
        """It should Activate a suspended Customer"""
        test_customer = CustomerFactory(status="suspended")
        test_customer.create()

        response = self.client.put(f"{BASE_URL}/{test_customer.id}/activate")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "active")

    def test_activate_nonexistent_customer(self):
        """It should return 404 when activating a Customer that does not exist"""
        response = self.client.put(f"{BASE_URL}/0/activate")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    def test_activated_status_persists(self):
        """It should persist the active status after an activate call and GET"""
        test_customer = CustomerFactory(status="suspended")
        test_customer.create()

        self.client.put(f"{BASE_URL}/{test_customer.id}/activate")

        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "active")

    def test_suspend_already_suspended_customer(self):
        """It should remain suspended when suspending an already suspended Customer"""
        test_customer = CustomerFactory(status="suspended")
        test_customer.create()

        response = self.client.put(f"{BASE_URL}/{test_customer.id}/suspend")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "suspended")

    def test_activate_already_active_customer(self):
        """It should remain active when activating an already active Customer"""
        test_customer = CustomerFactory(status="active")
        test_customer.create()

        response = self.client.put(f"{BASE_URL}/{test_customer.id}/activate")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "active")
