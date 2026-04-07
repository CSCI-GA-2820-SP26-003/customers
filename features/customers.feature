Feature: The store service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my customers

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