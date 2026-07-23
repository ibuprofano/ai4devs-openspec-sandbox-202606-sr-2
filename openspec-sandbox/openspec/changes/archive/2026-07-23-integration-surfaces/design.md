## Context

`core-engine-foundation` deliberately reserved `src/text2gherkin/adapters/` for exactly this work and established the rule that adapters only call `text2gherkin.engine.convert()`. This change fills that package with three adapters. It's cross-cutting by nature (three separate frameworks: Typer, FastAPI, the MCP SDK) but each adapter individually is a thin wrapper, so the design decisions below are mostly about keeping them thin and consistent with each other, not about new core logic.

## Goals / Non-Goals

**Goals:**
- Three adapters that each do nothing but: accept input in their protocol's idiom, call `convert()`, return the result (or a translated error) in their protocol's idiom
- Consistent error handling: `convert()`'s `ValueError` (exhausted retries) is translated into each protocol's normal error-reporting mechanism, not left to crash unhandled
- Each adapter independently testable without needing the others or a live deployment

**Non-Goals:**
- Any new conversion logic, prompt changes, or validation changes — those belong to `core-engine-foundation`/`core-engine-verification`, not here
- Authentication, rate limiting, or request logging on the API — out of scope until a real deployment need arises
- Docker packaging — that's `PLAN.md` Group 4, a separate change

## Decisions

**1. CLI: Typer app with file-or-stdin input, file-or-stdout output**
Alternative considered: file arguments only (as `config.yaml`'s example literally shows: `text2gherkin convert input.txt -o output.feature`).
Chosen: keep the file-argument form as the primary documented usage, but make the input file argument optional and read from stdin when omitted, and make `-o` optional and write to stdout when omitted. This is standard Unix CLI convention (enables piping: `cat input.txt | text2gherkin convert | tee output.feature`) and costs nothing extra to support. On `convert()` raising, print the error to stderr and exit with a non-zero status code.

**2. HTTP API: single `POST /convert`, JSON in/out, Pydantic request/response models**
Chosen: `{"text": str}` request, `{"gherkin": str}` response — matches the proposal's example exactly. On `convert()` raising `ValueError` (exhausted retries), return **502 Bad Gateway** with `{"detail": "<error message>"}`: the failure is upstream (the LLM didn't produce valid output after retries), not a malformed client request, so 4xx would misattribute the fault. FastAPI's automatic request validation (empty/missing `text`) already produces 422 for genuinely malformed requests, which is left as FastAPI's default behavior.

**3. MCP server: official `mcp` Python SDK's `FastMCP` helper, one tool named `convert`**
Alternative considered: implement the MCP protocol's JSON-RPC framing by hand.
Chosen: the official SDK (verified on PyPI, v1.28.1) — `FastMCP` turns a decorated Python function into a full MCP tool with schema generation from type hints, which is exactly the `convert(text: str) -> str` signature already in place. Hand-rolling the protocol would duplicate what the SDK already does correctly and is unnecessary complexity for one tool.

**4. MCP smoke test (task 14) uses the SDK's in-process client, not an external agent**
Alternative considered: require a real external MCP client (e.g. an actual Claude Code session) to connect to the running server for the smoke test, as `PLAN.md`'s task wording ("e.g. Claude Code") suggests.
Chosen: the `mcp` SDK ships client-side session objects that can connect to a server over an in-memory or stdio transport pair within the same process/test — this is the standard way MCP servers are smoke-tested in the SDK's own test suite, and it doesn't require a separate running agent product to verify the tool is correctly registered and callable. This is a testing-approach decision, not a scope change: an external agent could still connect to the same server later, since the server itself doesn't know or care what kind of client connects.

**5. `uvicorn` added as a dependency for the API adapter**
Not previously listed in `openspec/config.yaml`'s tech stack, but FastAPI needs an ASGI server to actually run outside of tests (`TestClient` alone is sufficient for automated tests but doesn't serve real requests). This is a necessary companion to the already-decided FastAPI choice, not a new architectural decision.

## Risks / Trade-offs

- [Three frameworks in one change increases the surface area to get wrong] → Mitigated by each adapter being a thin, independently-testable wrapper (Goals), and by writing tests for each one (CLI invocation tests, API `TestClient` tests, MCP in-process client test) before moving to the next.
- [502 for LLM failures (Decision 2) is a judgment call — some API consumers might expect 500] → Accepted trade-off: 502 more precisely communicates "upstream service failed," which is accurate here (the upstream LLM), and is documented so consumers know what to expect.
- [The MCP smoke test (Decision 4) doesn't prove Claude Code specifically can use the tool, only that the protocol implementation is correct] → Accepted trade-off: protocol-level correctness is what's testable in this environment; a manual check with a real MCP client remains a reasonable follow-up outside this change if desired.

## Open Questions

None outstanding — the three adapters' shapes, error handling, and testing approaches are settled by the decisions above.
