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

from flask import jsonify, request, url_for, abort, render_template
from flask import current_app as app  # Import Flask application
from service.models import Customer
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Customer REST API Service",
            version="1.0",
            paths=url_for("create_customers", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# ADMIN UI
######################################################################
@app.route("/ui")
def admin_ui():
    """Customer administration page"""
    return render_template("index.html")


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW CUSTOMER
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based on the data in the body that is posted
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")

    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = request.base_url + "/" + str(customer.id)

    app.logger.info("Customer with ID: %d created.", customer.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# READ A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """
    Retrieve a single Customer

    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request to Retrieve a customer with id [%s]", customer_id)

    # Attempt to find the Pet and abort if not found
    customer = Customer.find(customer_id)
    if not customer:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' was not found.",
        )

    app.logger.info("Returning Customer: %s", customer.name)
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
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

    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
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
    return jsonify(results), status.HTTP_200_OK


######################################################################
# SUSPEND A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>/suspend", methods=["PUT"])
def suspend_customer(customer_id):
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
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# ACTIVATE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>/activate", methods=["PUT"])
def activate_customer(customer_id):
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
    return jsonify(customer.serialize()), status.HTTP_200_OK


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


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based the id specified in the path
    """
    app.logger.info("Request to delete customer with id: %s", customer_id)

    customer = Customer.find(customer_id)
    if customer:
        customer.delete()

    return "", status.HTTP_204_NO_CONTENT
