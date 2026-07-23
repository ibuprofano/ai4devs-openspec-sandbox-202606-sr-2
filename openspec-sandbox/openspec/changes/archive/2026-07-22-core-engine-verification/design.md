## Context

`core-engine-foundation` built `convert()` but its retry logic and end-to-end behavior were only checked with mocked LLM calls during that change's implementation session, plus one live call that was never completed (task 6.4 was left pending — blocked on API credits, not on code). This change adds the permanent, repeatable test suite that `core-engine-foundation`'s tasks.md anticipated as a separate step (Group 2 in the project plan).

A concrete constraint discovered while implementing `core-engine-foundation`: a configured LLM API key with available credits is not guaranteed to be present in every environment that runs this test suite (this repo's own dev environment hit exactly that gap). The test design has to account for that rather than assume a live key is always available.

## Goals / Non-Goals

**Goals:**
- A fixture format that's easy to add to (3-5 fixtures now, more later) without writing new test code per fixture
- Tests that catch a broken prompt/wiring regression, not just a broken import
- The retry-on-invalid-output path exercised by an automated test, not just manual spot-checks
- Tests that behave sanely when no LLM API key/credits are available (skip with a clear reason, not a hard failure)

**Non-Goals:**
- Changing `convert()`, the prompt template, or the validator's behavior — this change only adds tests around the existing implementation (fixing bugs the tests happen to surface is in scope as a side effect, changing intended behavior is not)
- Exact-string-match assertions against LLM output — covered under Decisions, this is deliberately not attempted
- CI pipeline configuration — out of scope; this change only produces the pytest suite itself

## Decisions

**1. Golden fixtures as paired plain-text files, not a single JSON/YAML file**
Alternative considered: one `fixtures.json` containing all input/output pairs.
Chosen: one directory per fixture (e.g. `tests/fixtures/add_to_cart/input.txt` + `tests/fixtures/add_to_cart/expected.feature`), discovered by pytest via directory listing. This keeps each fixture readable as a real `.feature` file (diffable, syntax-highlightable) rather than an escaped string inside JSON, and matches the shape golden-file tests conventionally take.

**2. Assert structural/semantic match, not exact string match**
Alternative considered: assert `convert(input) == expected_output` verbatim.
Chosen: assert (a) the output parses as valid Gherkin via `validate_gherkin()`, and (b) the output has the same number of scenarios with the same step count per scenario, in order, as the expected fixture — **not** matching `Scenario:` title wording. LLM output is not byte-identical across runs even at low temperature — an exact-match assertion would make the suite flaky for reasons unrelated to actual regressions, and this includes scenario titles: running the golden-file tests for real (once API credits were available) showed the model reliably reproducing the same scenario count and step count while phrasing titles differently each run (e.g. "Greeting the user by name" vs "User receives a personalized greeting" for the same steps). Structural comparison still catches the failure modes that matter: wrong number of scenarios, missing steps, invalid syntax.

**3. Retry-path test uses a mocked LLM call, not a live one**
Alternative considered: find or construct an input that reliably makes the real model produce invalid Gherkin on the first attempt, to exercise retry live.
Chosen: mock `text2gherkin.engine.call_llm` to return invalid text on the first call and valid text on the second (the same technique used to sanity-check this logic during `core-engine-foundation`'s implementation). Relying on the live model to fail in a specific, reproducible way is not something the test suite can depend on — model behavior may change over time and shouldn't be relied on to fail.

**4. Golden-file tests (live LLM) are skipped, not failed, when no usable API key is present**
Alternative considered: let tests fail with a connection/billing error when no key is configured, same as what happened running task 6.4 manually.
Chosen: a pytest fixture checks for a usable LLM configuration (e.g. `ANTHROPIC_API_KEY` set) at collection time and skips the golden-file tests with an explicit reason ("no LLM API key configured") if absent. The mocked retry-path test (Decision 3) has no such dependency and always runs. This means `pytest` produces a clear, actionable skip rather than a wall of HTTP errors in an environment without credits — directly informed by hitting that exact situation in this repo.

## Risks / Trade-offs

- [Structural comparison (Decision 2) could pass a test even if step wording drifts significantly from what's expected] → Accepted trade-off: catching gross regressions (wrong scenario count, invalid syntax) matters more here than pixel-perfect wording, and exact match would be worse (constant false failures unrelated to real bugs).
- [Skipping golden-file tests without a key (Decision 4) means this suite alone can pass in an environment that never actually exercises the real LLM path] → Mitigated by the suite reporting skipped tests explicitly (visible in pytest output, not silently green), and by the mocked retry test still covering the wiring logic even when skipped.
- [Golden-file tests that do run against a live model cost a small amount per run] → Accepted trade-off inherent to testing an LLM-backed function at all; kept to 3-5 fixtures to bound the cost.

## Open Questions

None outstanding — the fixture format, comparison strategy, and API-key-skip behavior are settled by the decisions above and don't block moving to tasks.
