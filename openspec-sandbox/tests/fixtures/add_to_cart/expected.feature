Feature: Add item to cart

  Scenario: Adding an in-stock item to the cart
    Given a logged-in user
    And the item is in stock
    When the user adds the item to their cart
    Then the item appears in the cart

  Scenario: Attempting to add an out-of-stock item
    Given a logged-in user
    And the item is out of stock
    When the user adds the item to their cart
    Then the user sees an error message
    And the cart does not change
