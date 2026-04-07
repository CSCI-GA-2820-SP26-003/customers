Feature: Customer Administration UI
    As a Store Manager
    I need a web UI for managing customers
    So that I can create, read, update, delete, list, query, suspend, and activate customers

Background:
    Given the following customers
        | name           | address              | status    |
        | John Adams     | 123 Main Street      | active    |
        | Mary Johnson   | 456 Oak Avenue       | active    |
        | Bob Smith      | 789 Pine Road        | suspended |
        | Alice Brown    | 321 Elm Boulevard    | suspended |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Administration" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "customer_name" field to "Test Customer"
    And I set the "customer_address" field to "999 Test Avenue"
    And I press the "Create" button
    Then I should see "Success" in the flash message
    And I should see "Test Customer" in the "customer_name" field
    And I should see "999 Test Avenue" in the "customer_address" field

Scenario: Read a Customer
    When I visit the "Home Page"
    And I set the "search_id" field to the id of "John Adams"
    And I press the "Retrieve by ID" button
    Then I should see "Success" in the flash message
    And I should see "John Adams" in the "customer_name" field
    And I should see "123 Main Street" in the "customer_address" field

Scenario: Read a Customer That Does Not Exist
    When I visit the "Home Page"
    And I set the "search_id" field to "0"
    And I press the "Retrieve by ID" button
    Then I should see "not found" in the flash message

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "search_id" field to the id of "John Adams"
    And I press the "Retrieve by ID" button
    Then I should see "Success" in the flash message
    When I set the "customer_name" field to "John Adams Updated"
    And I set the "customer_address" field to "999 Updated Street"
    And I press the "Update" button
    Then I should see "Success" in the flash message
    And I should see "John Adams Updated" in the "customer_name" field
    And I should see "999 Updated Street" in the "customer_address" field

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "search_id" field to the id of "Alice Brown"
    And I press the "Retrieve by ID" button
    Then I should see "Success" in the flash message
    When I press the "Delete" button
    Then I should see "Deleted" in the flash message

Scenario: List All Customers
    When I visit the "Home Page"
    And I press the "List All" button
    Then I should see "Success" in the flash message
    And I should see "John Adams" in the results
    And I should see "Mary Johnson" in the results
    And I should see "Bob Smith" in the results
    And I should see "Alice Brown" in the results

Scenario: Query a Customer by Name
    When I visit the "Home Page"
    And I set the "search_name" field to "John Adams"
    And I press the "Query by Name" button
    Then I should see "Success" in the flash message
    And I should see "John Adams" in the results

Scenario: Suspend a Customer
    When I visit the "Home Page"
    And I set the "search_id" field to the id of "John Adams"
    And I press the "Retrieve by ID" button
    Then I should see "Success" in the flash message
    When I press the "Suspend" button
    Then I should see "Success" in the flash message
    And I should see "suspended" in the "customer_status" field

Scenario: Activate a Customer
    When I visit the "Home Page"
    And I set the "search_id" field to the id of "Bob Smith"
    And I press the "Retrieve by ID" button
    Then I should see "Success" in the flash message
    When I press the "Activate" button
    Then I should see "Success" in the flash message
    And I should see "active" in the "customer_status" field
