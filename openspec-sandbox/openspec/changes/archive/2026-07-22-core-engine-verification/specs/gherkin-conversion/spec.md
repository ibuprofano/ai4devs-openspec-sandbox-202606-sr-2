## MODIFIED Requirements

### Requirement: Convert free-form text to Gherkin
The system SHALL provide a function `convert(text: str) -> str` that translates free-form text describing user actions into a Gherkin `.feature` document, preserving the domain nouns and verbs present in the input.

#### Scenario: Converting a valid action description
- **WHEN** `convert()` is called with text describing one or more user actions and their expected outcomes
- **THEN** it returns a string containing a `Feature:` block with at least one `Scenario:` and Given/When/Then steps that reflect the actions described in the input

#### Scenario: Preserving domain terms from the input
- **WHEN** the input text names specific entities or actions (e.g. "cart", "out of stock", "logged-in user")
- **THEN** the generated Given/When/Then steps use those same terms rather than generic placeholders

#### Scenario: Splitting one input into multiple scenarios
- **WHEN** the input text describes more than one distinct outcome (e.g. a success path and a failure/edge-case path)
- **THEN** `convert()` returns a `Feature:` block containing a separate `Scenario:` for each distinct outcome, rather than merging them into one
