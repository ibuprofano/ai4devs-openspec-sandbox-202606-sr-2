## Why

There is currently no way to turn free-form text describing user actions (requirements, user stories, meeting notes, manual QA scripts, chat transcripts) into a valid BDD/Gherkin `.feature` file. Every downstream interface planned for this utility (CLI, REST API, MCP tool) depends on one thing existing first: a core conversion function that reliably produces syntactically valid Gherkin. This change builds that core, in isolation, before any adapter is built on top of it — so later work doesn't get done twice if the core's interface or validation approach needs to change.

## What Changes

- Scaffold the Python package (`pyproject.toml`, src layout, pinned dependencies: LiteLLM, gherkin-official, Typer, FastAPI, pytest)
- Define the core `convert(text: str) -> str` function signature and separate the engine module from future adapter modules
- Add versioned prompt template file(s) with few-shot examples for NL → Gherkin translation
- Implement an LLM abstraction layer (LiteLLM) with provider/model configurable via env vars, defaulting to Claude Sonnet 5
- Implement a Gherkin validation layer (`gherkin-official`) that parses candidate output and reports valid/invalid + error detail
- Wire `convert()` end-to-end: call the LLM through the prompt template, validate the result, and reject-and-retry when the output isn't valid Gherkin

Out of scope for this change: CLI, REST API, MCP wrapper, Docker packaging, and the golden-file test suite — these depend on this core and are separate changes (Groups 2-4 in the project plan).

## Capabilities

### New Capabilities
- `gherkin-conversion`: Converts free-form text describing user actions into a valid Gherkin `.feature` file, via an LLM call constrained by a versioned prompt template and checked by a Gherkin syntax validator with reject-and-retry on invalid output.

### Modified Capabilities
(none — this is a greenfield capability)

## Example Input → Expected Output

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

This pair anchors what "correct" means for this capability: one input can legitimately expand into multiple scenarios, existing domain nouns/verbs from the input should be preserved in the Given/When/Then steps, and the output must parse as valid Gherkin.

## Impact

- New Python package (no existing code is modified — this is a new standalone utility)
- New dependencies: LiteLLM, gherkin-official, Typer, FastAPI, pytest (per `openspec/config.yaml` tech stack)
- No persistent storage: this capability is stateless by design (input text in, `.feature` text out). No database is introduced by this change — an audit trail of past conversions remains an optional, unbuilt future add-on, not a dependency of the core engine.
- No impact on other systems, since nothing consumes this utility yet (adapters are later changes)
