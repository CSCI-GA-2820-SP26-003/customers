Feature: The pet store service back-end
    As a Pet Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my pets

Background:
    Given the following pets
        | first_name  | last_name | email               | active  |
        | John        | Adams     | john@example.com    | TRUE    |
        | Custer      | William   | custer@example.com  | TRUE    |
        | Gunther     | Brine     | gunther@example.com | FALSE   |
        | Samuel      | Hart      | samuel@example.com  | False   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see " Customer Administration" in the title
    And I should not see "404 Not Found"