Feature: Delete post

  Scenario: Editor attempts to delete another user's post
    Given an editor
    And a post belonging to another user
    When the editor tries to delete the post
    Then the editor sees a "Permission denied" message
    And the post remains
