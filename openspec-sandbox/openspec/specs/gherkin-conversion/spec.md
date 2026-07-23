# gherkin-conversion Specification

## Purpose
Converts free-form text describing user actions into a valid Gherkin `.feature` file, via an LLM call constrained by a versioned prompt template and checked by a Gherkin syntax validator with reject-and-retry on invalid output.

## Requirements

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

### Requirement: Validate generated Gherkin syntax
The system SHALL validate every candidate output against the official Gherkin grammar before returning it, and SHALL NOT return output that fails to parse.

#### Scenario: Valid output is returned as-is
- **WHEN** the LLM's candidate output parses successfully as Gherkin
- **THEN** `convert()` returns that output unchanged

#### Scenario: Invalid output triggers a retry
- **WHEN** the LLM's candidate output fails to parse as Gherkin
- **THEN** the system retries the LLM call, including the parser's error message as corrective feedback, up to a bounded number of attempts

#### Scenario: Output still invalid after retries are exhausted
- **WHEN** every retry attempt's output still fails to parse as Gherkin
- **THEN** `convert()` raises an error rather than returning invalid Gherkin text

### Requirement: Provider-agnostic LLM configuration
The system SHALL route all LLM calls through a provider-agnostic abstraction, defaulting to Claude Sonnet 5, and SHALL allow the provider and model to be overridden via configuration without a code change.

#### Scenario: Default model used when no configuration is given
- **WHEN** `convert()` is called with no provider/model environment variables set
- **THEN** the system uses the default Claude Sonnet 5 model for the translation

#### Scenario: Overriding the provider/model via environment variable
- **WHEN** an environment variable specifying a different provider/model is set before `convert()` is called
- **THEN** the system routes the LLM call to that provider/model instead of the default

### Requirement: Stateless operation
The system SHALL NOT persist any input text, generated output, or conversion history between calls.

#### Scenario: Repeated calls do not depend on prior calls
- **WHEN** `convert()` is called multiple times in sequence with different inputs
- **THEN** each call's output depends only on its own input text and configuration, not on any previous call
