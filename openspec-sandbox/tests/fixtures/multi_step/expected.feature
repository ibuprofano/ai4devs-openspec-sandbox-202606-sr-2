Feature: Download invoice

  Scenario: Downloading an invoice as an eligible user
    Given a registered user with a verified email
    And the user has an active subscription
    When the user opens the billing page
    And the user clicks "Download Invoice"
    Then the system generates a PDF invoice
    And the download starts
