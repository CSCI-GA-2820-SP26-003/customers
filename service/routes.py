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
Customer Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Customer
"""

from flask import request, abort
from flask import current_app as app  # Import Flask application
from flask_restx import Namespace, Resource, fields
from service.models import Customer
from service.common import status  # HTTP Status Codes

######################################################################
# Configure the namespace for customer resources
######################################################################
ns = Namespace("customers", description="Customer operations")

######################################################################
# API Models for Swagger documentation
######################################################################
create_model = ns.model(
    "CustomerCreate",
    {
        "name": fields.String(required=True, description="Customer name"),
        "address": fields.String(required=True, description="Customer address"),
        "status": fields.String(
            description="Customer status (active or suspended)", example="active"
        ),
    },
)

customer_model = ns.model(
    "Customer",
    {
        "id": fields.Integer(
            readonly=True, description="The customer unique identifier"
        ),
        "name": fields.String(required=True, description="Customer name"),
        "address": fields.String(required=True, description="Customer address"),
        "status": fields.String(
            description="Customer status (active or suspended)", example="active"
        ),
    },
)

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# LIST ALL CUSTOMERS / CREATE A NEW CUSTOMER
######################################################################
@ns.route("", strict_slashes=False)
class CustomerCollection(Resource):
    """Handles all interactions with collections of Customers"""

    @ns.doc("list_customers")
    @ns.param("name", "Filter customers by name")
    @ns.marshal_list_with(customer_model)
    def get(self):
        """Returns all of the Customers"""
        app.logger.info("Request for the customer list")

        name = request.args.get("name")
        if name:
            app.logger.info("Find by name: %s", name)
            customers = Customer.find_by_name(name)
        else:
            app.logger.info("Find all")
            customers = Customer.all()

        results = [customer.serialize() for customer in customers]
        app.logger.info("Returning %d customers", len(results))
        return results, status.HTTP_200_OK

    @ns.doc("create_customer")
    @ns.expect(create_model)
    @ns.response(201, "Customer created successfully")
    @ns.response(400, "Validation error")
    @ns.response(415, "Unsupported media type")
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based on the data in the body that is posted
        """
        app.logger.info("Request to create a customer")
        check_content_type("application/json")

        customer = Customer()
        customer.deserialize(request.get_json())
        if (
            not customer.name
            or not customer.name.strip()
            or not customer.address
            or not customer.address.strip()
        ):
            abort(
                status.HTTP_400_BAD_REQUEST,
                "Name and Address are required and cannot be empty",
            )
        customer.create()
        message = customer.serialize()
        location_url = request.base_url.rstrip("/") + "/" + str(customer.id)

        app.logger.info("Customer with ID: %d created.", customer.id)
        return message, status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# READ / UPDATE / DELETE A CUSTOMER
######################################################################
@ns.route("/<int:customer_id>", strict_slashes=False)
@ns.param("customer_id", "The Customer identifier")
class CustomerResource(Resource):
    """Handles all interactions with a single Customer"""

    @ns.doc("get_customer")
    @ns.marshal_with(customer_model)
    @ns.response(404, "Customer not found")
    def get(self, customer_id):
        """
        Retrieve a single Customer

        This endpoint will return a Customer based on it's id
        """
        app.logger.info("Request to Retrieve a customer with id [%s]", customer_id)

        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )

        app.logger.info("Returning Customer: %s", customer.name)
        return customer.serialize(), status.HTTP_200_OK

    @ns.doc("update_customer")
    @ns.expect(create_model, validate=True)
    @ns.marshal_with(customer_model)
    @ns.response(404, "Customer not found")
    def put(self, customer_id):
        """
        Update a Customer

        This endpoint will update a Customer based the body that is posted
        """
        app.logger.info("Request to update customer with id: %s", customer_id)

        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )

        customer.deserialize(request.get_json())
        customer.id = customer_id
        customer.update()

        return customer.serialize(), status.HTTP_200_OK

    @ns.doc("delete_customer")
    @ns.response(204, "Customer deleted")
    @ns.response(404, "Customer not found")
    def delete(self, customer_id):
        """
        Delete a Customer

        This endpoint will delete a Customer based the id specified in the path
        """
        app.logger.info("Request to delete customer with id: %s", customer_id)

        customer = Customer.find(customer_id)
        if customer:
            customer.delete()

        return "", status.HTTP_204_NO_CONTENT


######################################################################
# SUSPEND A CUSTOMER
######################################################################
@ns.route("/<int:customer_id>/suspend", strict_slashes=False)
@ns.param("customer_id", "The Customer identifier")
class SuspendCustomer(Resource):
    """Endpoint to suspend a Customer"""

    @ns.doc("suspend_customer")
    @ns.marshal_with(customer_model)
    @ns.response(404, "Customer not found")
    def put(self, customer_id):
        """
        Suspend a Customer

        This endpoint will suspend a Customer based on the id specified in the path
        """
        app.logger.info("Request to suspend customer with id: %s", customer_id)

        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )

        customer.status = "suspended"
        customer.update()

        app.logger.info("Customer with ID: %d suspended.", customer.id)
        return customer.serialize(), status.HTTP_200_OK


######################################################################
# ACTIVATE A CUSTOMER
######################################################################
@ns.route("/<int:customer_id>/activate", strict_slashes=False)
@ns.param("customer_id", "The Customer identifier")
class ActivateCustomer(Resource):
    """Endpoint to activate a Customer"""

    @ns.doc("activate_customer")
    @ns.marshal_with(customer_model)
    @ns.response(404, "Customer not found")
    def put(self, customer_id):
        """
        Activate a Customer

        This endpoint will activate a Customer based on the id specified in the path
        """
        app.logger.info("Request to activate customer with id: %s", customer_id)

        customer = Customer.find(customer_id)
        if not customer:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Customer with id '{customer_id}' was not found.",
            )

        customer.status = "active"
        customer.update()

        app.logger.info("Customer with ID: %d activated.", customer.id)
        return customer.serialize(), status.HTTP_200_OK


######################################################################
# UTILITY FUNCTIONS
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] != content_type:
        app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )
