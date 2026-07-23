## ADDED Requirements

### Requirement: Convert text via MCP tool
The system SHALL expose a `convert` tool over the Model Context Protocol that an MCP client can discover and call with text input, returning the converted Gherkin text, using the existing conversion engine.

#### Scenario: Tool is discoverable
- **WHEN** an MCP client lists the tools available from the server
- **THEN** a tool named `convert` is present in the list

#### Scenario: Calling the tool with valid input
- **WHEN** an MCP client calls the `convert` tool with text describing a user action
- **THEN** the tool returns the converted Gherkin text as its result

#### Scenario: Calling the tool with input that fails conversion
- **WHEN** the conversion engine raises an error (e.g. exhausted retries on invalid output) while handling a tool call
- **THEN** the tool call returns an MCP error result describing the failure, rather than crashing the server
