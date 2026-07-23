## Context

This is a greenfield Python package. Nothing exists yet — no repo structure, no dependency manifest. This design covers only the core engine (Group 1 of the project plan): the package scaffold, the `convert(text: str) -> str` function, prompt templates, the LLM abstraction, and Gherkin validation. CLI, REST API, MCP wrapper, and Docker packaging are later changes and depend on this one; they are referenced here only to justify boundaries, not designed in detail.

## Goals / Non-Goals

**Goals:**
- A single, pure, synchronous function `convert(text: str) -> str` that is the only thing later adapters (CLI/API/MCP) call
- Provider-agnostic LLM access, so the utility isn't locked to Anthropic
- Guaranteed syntactic validity of returned Gherkin (never hand back unparseable output)
- Prompt content kept out of code, so translation quality can be tuned without a code change

**Non-Goals:**
- Building any adapter (CLI, API, MCP) — those are separate changes on top of this core
- Persistence of any kind — this function is stateless; no DB, no cache, no history
- Semantic correctness grading of the generated Gherkin (only syntactic validity is checked programmatically; semantic quality is judged by the golden-file tests in Group 2, not by this core function itself)

## Decisions

**1. LLM access via LiteLLM, not the Anthropic SDK directly**
Alternative considered: call the Anthropic SDK directly, since Claude Sonnet 5 is the default model.
Chosen: LiteLLM, because `openspec/config.yaml` establishes that this utility must be "integrable across different tech stacks and contexts" — a consumer already standardized on OpenAI/Azure/Bedrock shouldn't be blocked from swapping providers. LiteLLM gives a single call interface across providers; the provider/model is read from environment variables (e.g. `TEXT2GHERKIN_MODEL`, defaulting to a Claude Sonnet 5 model string), so switching providers is a config change, not a code change.

**2. Prompt templates as versioned plain files, not inline strings**
Alternative considered: embed the prompt as a Python string constant in the engine module.
Chosen: plain template file(s) (e.g. `src/text2gherkin/prompts/convert_v1.md`) loaded at call time, containing the instruction plus few-shot examples (using the input/output pair from the proposal as the seed example). This lets translation quality be iterated on without touching `convert()`'s code, and keeps a version identifier in the filename so a future prompt change is traceable.

**3. Validation via `gherkin-official`, with reject-and-retry, not a custom parser**
Alternative considered: write a lightweight regex/structural check for `Feature:`/`Scenario:`/`Given/When/Then` lines.
Chosen: `gherkin-official` (Cucumber's own reference parser) because a hand-rolled check would only catch gross formatting errors, not the same syntax Cucumber itself enforces. On invalid output, `convert()` retries the LLM call (bounded, e.g. 2 retries) with the parser's error message appended to the prompt as corrective feedback, then raises if still invalid after retries are exhausted — it does not silently return invalid Gherkin.

**4. Module layout: engine vs. adapters, from day one**
`src/text2gherkin/engine.py` (the `convert()` function and its internals: LLM call, validation, retry loop) is kept separate from any future adapter module. No CLI/API/MCP code exists yet in this change, but the separation is established now specifically so Groups 3's adapters are additions, not refactors of engine internals.

## Risks / Trade-offs

- [LLM output is inherently non-deterministic] → Mitigated by the validator (guarantees syntactic validity) and the retry loop (gives the model a second chance using its own parser error as feedback); semantic quality is a testing concern (Group 2), not something this design can fully guarantee.
- [LiteLLM abstraction adds a dependency and a layer of indirection versus calling Anthropic directly] → Accepted trade-off: the integrability requirement in `config.yaml` outweighs the marginal complexity, and LiteLLM's interface is thin enough that it doesn't obscure provider-specific errors.
- [Retry loop could mask a systematically broken prompt by quietly succeeding on the Nth attempt] → Mitigated by Group 2's test suite explicitly asserting on the forced-invalid-output retry path, so a prompt regression that requires retries to pass is visible in test output, not just in production latency.

## Migration Plan

Not applicable — this is a new package with no existing users or deployed version to migrate from.

## Open Questions

- Exact retry count and backoff (if any) before `convert()` raises — left as an implementation detail for Group 1's tasks rather than a design-level decision, since it doesn't affect the public interface or other capabilities.
- Whether the prompt template format should support multiple few-shot examples from day one or start with just the one in the proposal — left to implementation; adding more examples later doesn't change `convert()`'s signature or this design's decisions.
