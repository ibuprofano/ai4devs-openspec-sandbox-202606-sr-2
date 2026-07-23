# docker-packaging Specification

## Purpose
Distributes the system as a single Docker image that bundles both the CLI and the HTTP API, so it can run without a local Python installation. The image defaults to running the API, but its command can be overridden to run the CLI instead, using the same installed code.

## Requirements

### Requirement: Distributable as a single Docker image
The system SHALL be distributable as a single Docker image that bundles both the CLI and the HTTP API, runnable without a local Python installation.

#### Scenario: Running the image starts the API by default
- **WHEN** the image is run with no additional arguments
- **THEN** the HTTP API starts and is reachable on the container's exposed port

#### Scenario: Overriding the image's command runs the CLI
- **WHEN** the image is run with `text2gherkin convert` (and its arguments) as the container command
- **THEN** the CLI runs inside the container instead of the API, using the same installed code

#### Scenario: No API key baked into the image
- **WHEN** the image is inspected or run without an API key passed at run time
- **THEN** no provider API key is present in the image itself; conversion requests fail the same way they would locally without a configured key
