## 1. Golden Fixtures

- [x] 1.1 Create `tests/fixtures/` with one subdirectory per fixture, each containing `input.txt` and `expected.feature`
- [x] 1.2 Add fixture `add_to_cart`: the input/output pair already used in `proposal.md` and to seed the prompt template (covers: one input producing multiple scenarios)
- [x] 1.3 Add fixture `single_scenario`: a simple one-outcome input (covers: the minimal single-`Scenario:` case)
- [x] 1.4 Add fixture `multi_step`: an input requiring a chain of `Given`/`And` steps (covers: multi-step preconditions)
- [x] 1.5 Add fixture `permission_denied` (or similar edge case): an action that's blocked by a precondition, distinct from the out-of-stock case in `add_to_cart` (covers: a second branching/edge-case shape)

## 2. Test Infrastructure

- [x] 2.1 Add a pytest fixture that checks for a usable LLM API key (e.g. `ANTHROPIC_API_KEY`) and skips dependent tests with an explicit reason ("no LLM API key configured") when absent
- [x] 2.2 Add a structural-comparison helper that parses actual and expected Gherkin text and asserts matching `Scenario:` titles and step counts (not exact string match)
- [x] 2.3 Parse the structural-comparison helper's own output (both actual and expected) with `gherkin-official` as part of its assertions, confirming both sides are valid Gherkin before comparing structure

## 3. Golden-File Tests (live LLM, skipped without a key)

- [x] 3.1 Write a parametrized pytest test that runs `convert()` against every fixture under `tests/fixtures/` and asserts the result via the structural-comparison helper (task 2.2), using the skip fixture (task 2.1)
- [x] 3.2 Run all fixtures once locally with a configured API key and confirm they pass, or fix `src/text2gherkin/` if a fixture reveals a real bug (per design: fixing bugs the tests surface is in scope, changing intended behavior is not) — all 4 passed after fixing the comparison helper (see design.md Decision 2 update; the bug was in the test helper's title-matching, not in `src/text2gherkin/`)

## 4. Retry-Path Tests (mocked, always run)

- [x] 4.1 Write a test that mocks `text2gherkin.engine.call_llm` to return invalid Gherkin then valid Gherkin, asserting `convert()` retries once and returns the valid result
- [x] 4.2 Write a test that mocks `call_llm` to always return invalid Gherkin, asserting `convert()` raises after exhausted retries, and that the raised error message includes the parser's error detail
- [x] 4.3 Run the full test suite (`pytest`) and confirm the retry-path tests (task 4) pass regardless of API key presence, and the golden-file tests (task 3) either pass or skip cleanly depending on key presence — verified both branches: with key, 6/6 passed; without key, 2 passed + 4 skipped cleanly
