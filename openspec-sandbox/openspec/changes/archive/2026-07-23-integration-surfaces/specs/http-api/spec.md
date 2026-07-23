## ADDED Requirements

### Requirement: Convert text via HTTP API
The system SHALL provide a `POST /convert` endpoint that accepts a JSON body `{"text": string}` and returns a JSON body `{"gherkin": string}` containing the converted Gherkin text, using the existing conversion engine.

#### Scenario: Successful conversion
- **WHEN** a `POST /convert` request is sent with a valid JSON body containing `text`
- **THEN** the response has status 200 and a JSON body with a `gherkin` field containing the converted text

#### Scenario: Conversion failure returns a 502
- **WHEN** the conversion engine raises an error (e.g. exhausted retries on invalid output) while handling a request
- **THEN** the response has status 502 and a JSON body with a `detail` field describing the error

#### Scenario: Malformed request returns a 422
- **WHEN** a `POST /convert` request is sent with a missing or invalid `text` field
- **THEN** the response has status 422, per the framework's standard request validation
