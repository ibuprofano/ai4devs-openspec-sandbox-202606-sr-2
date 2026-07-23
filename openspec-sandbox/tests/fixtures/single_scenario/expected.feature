Feature: Greeting box

  Scenario: Greeting the user by name
    Given a user types their name into the greeting box
    When the user clicks "Say Hello"
    Then the page shows "Hello, <name>!" back to them
