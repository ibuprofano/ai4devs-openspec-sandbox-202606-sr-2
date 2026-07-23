# cli-interface Specification

## Purpose
Provides a command-line interface for converting free-form text to Gherkin, so users can run conversions from a terminal against files or piped input.

## Requirements

### Requirement: Convert text via CLI
The system SHALL provide a `text2gherkin convert` command-line command that reads input text from a file argument or stdin, converts it to Gherkin using the existing conversion engine, and writes the result to an output file (`-o`) or stdout.

#### Scenario: Converting from a file to a file
- **WHEN** the command is invoked with an input file argument and `-o <output file>`
- **THEN** the output file is created containing the converted Gherkin text

#### Scenario: Converting from stdin to stdout
- **WHEN** the command is invoked with no input file argument and no `-o` flag, and text is piped into stdin
- **THEN** the converted Gherkin text is written to stdout

#### Scenario: Exiting non-zero on conversion failure
- **WHEN** the conversion engine raises an error (e.g. exhausted retries on invalid output)
- **THEN** the command prints the error to stderr and exits with a non-zero status code
