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
Web Steps

Steps file for selenium-based web interactions.

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
from behave import when, then  # pylint: disable=no-name-in-module
from compare3 import expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@when('I visit the "{page_name}"')
def step_impl(context, page_name):
    """Navigate to the requested page"""
    if page_name == "Home Page":
        context.driver.get(f"{context.base_url}/ui")
    else:
        context.driver.get(f"{context.base_url}/{page_name.lower().replace(' ', '-')}")


@then('I should see "{text_string}" in the title')
def step_impl(context, text_string):
    """Check the document title for a string"""
    expect(text_string.strip() in context.driver.title).equal_to(True)


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    """Ensure a string is NOT visible on the page"""
    element = context.driver.find_element(By.TAG_NAME, "body")
    expect(text_string in element.text).equal_to(False)


@when('I set the "{element_id}" field to "{text_string}"')
def step_impl(context, element_id, text_string):
    """Clear an input field and type a value into it"""
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


@when('I set the "{element_id}" field to the id of "{name}"')
def step_impl(context, element_id, name):
    """Set an input field to the ID of a customer created in the background step"""
    customer_id = str(context.customer_list[name]["id"])
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(customer_id)


@when('I press the "{button_text}" button')
def step_impl(context, button_text):
    """Click a button by its visible label text"""
    xpath = f"//button[normalize-space(text())='{button_text}']"
    button = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    button.click()


@then('I should see "{text_string}" in the flash message')
def step_impl(context, text_string):
    """Check the flash message area for a string"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash-message"), text_string)
    )
    expect(found).equal_to(True)


@then('I should see "{text_string}" in the "{element_id}" field')
def step_impl(context, text_string, element_id):
    """Check that an input field contains the expected value"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), text_string)
    )
    expect(found).equal_to(True)
