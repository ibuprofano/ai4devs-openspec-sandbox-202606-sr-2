## 1. Package Scaffolding

- [x] 1.1 Create `pyproject.toml` with pinned dependencies: LiteLLM, gherkin-official, Typer, FastAPI, pytest
- [x] 1.2 Create the `src/text2gherkin/` package layout with separate modules reserved for the engine (this change) and future adapters (later changes)

## 2. Core Interface

- [x] 2.1 Define the `convert(text: str) -> str` function signature in `src/text2gherkin/engine.py`, stubbed with a placeholder return

## 3. Prompt Templates

- [x] 3.1 Add a versioned prompt template file (e.g. `src/text2gherkin/prompts/convert_v1.md`) with instructions for NL -> Gherkin translation
- [x] 3.2 Seed the template with a few-shot example using the input/output pair from `proposal.md`

## 4. LLM Abstraction

- [x] 4.1 Implement a LiteLLM-based call wrapper with provider/model read from environment variables, defaulting to a Claude Sonnet 5 model string
- [x] 4.2 Confirm the wrapper returns raw model text output without any Gherkin-specific post-processing (that belongs to validation, task 5.1)

## 5. Gherkin Validation

- [x] 5.1 Implement a validation function using `gherkin-official` that parses candidate text and returns valid/invalid plus error detail
- [x] 5.2 Manually verify the validator against one known-valid and one known-invalid `.feature` string before wiring it into `convert()`

## 6. Wire the Core Engine

- [x] 6.1 Wire `convert()`: call the LLM wrapper (task 4.1) with the prompt template (task 3.1), then validate the result with the validator (task 5.1)
- [x] 6.2 Implement reject-and-retry: on invalid output, retry the LLM call with the validator's error message appended as corrective feedback, up to a bounded attempt count
- [x] 6.3 Raise an error if output is still invalid after retries are exhausted, rather than returning invalid Gherkin
- [ ] 6.4 Run the validator (task 5.1) against `convert()`'s output for the example pair in `proposal.md` and confirm it parses successfully before considering this task group done
