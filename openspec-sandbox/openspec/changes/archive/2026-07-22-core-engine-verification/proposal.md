## Why

The `core-engine-foundation` change wired up `convert()` (LLM call → Gherkin validation → reject-and-retry), but that work was only checked with mocked LLM calls during implementation and one still-pending live call (blocked on API credits). There is no repeatable, versioned test suite that proves `convert()` behaves correctly across representative inputs, or that the retry-on-invalid-output path actually works. Without this, a future change to the prompt template or wiring logic could silently break conversion quality or the retry safety net, with nothing to catch it.

## What Changes

- Create a golden-file fixture set: 3-5 representative input texts paired with their expected `.feature` outputs, covering different shapes of input (single scenario, multiple scenarios from one input, an edge-case branch like the out-of-stock example from the proposal)
- Write a pytest suite that runs `convert()` against each fixture and asserts the output matches (or, where LLM output isn't deterministic enough for exact-match, asserts the output parses as valid Gherkin and contains the expected scenario structure)
- Add a forced-invalid-output test case that mocks the LLM call to return invalid Gherkin first and valid Gherkin second, asserting the retry path in `convert()` is actually exercised (not just manually spot-checked, as it was during `core-engine-foundation`'s implementation)

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `gherkin-conversion`: The "Convert free-form text to Gherkin" requirement gains an explicit scenario for splitting one input into multiple `Scenario:` blocks when it describes more than one distinct outcome — this behavior was implicit in the existing scenarios but not directly specified, and this change's golden fixtures test it directly (fixture #1 already produces two scenarios from one input). No other requirement's behavior changes; the rest of this change is test infrastructure, not new requirements.

## Example Input → Expected Output (golden fixture #1)

**Input text:**
```
A logged-in user adds an item to their cart. If the item is out of stock, they should see an error message instead and the cart should not change.
```

**Expected Gherkin output:**
```gherkin
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
```

This is the same pair already used to seed the prompt template in `core-engine-foundation`; it becomes the first golden fixture here. The other 2-4 fixtures will cover different input shapes (see What Changes).

## Impact

- Adds a `tests/` directory and a `tests/fixtures/` directory of paired input/output files — no production code in `src/text2gherkin/` is expected to change, though running these tests against a real LLM may surface bugs that require fixes there
- No new persistent storage: fixtures are static test files checked into the repo, not a database or runtime store
- Requires a configured LLM API key to run the golden-file tests against a live model (the mocked retry test does not); this is a test-execution prerequisite, not a new production dependency
