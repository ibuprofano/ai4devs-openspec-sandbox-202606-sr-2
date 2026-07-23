## 1. Dependencies & Packaging Prep

- [x] 1.1 Add `mcp` and `uvicorn` to `pyproject.toml` dependencies (Typer and FastAPI are already pinned)
- [x] 1.2 Add a `text2gherkin` console-script entry point to `pyproject.toml` pointing at the CLI's Typer app

## 2. CLI Adapter

- [x] 2.1 Implement `src/text2gherkin/adapters/cli.py`: a Typer app with a `convert` command, optional input file argument (reads stdin if omitted), optional `-o` output flag (writes stdout if omitted)
- [x] 2.2 Wire error handling: catch exceptions from `convert()`, print the error to stderr, exit with a non-zero status code

## 3. CLI Tests

- [x] 3.1 Test: invoking with an input file and `-o` produces the expected output file (mocked `convert()`)
- [x] 3.2 Test: invoking with piped stdin and no `-o` writes the expected output to stdout (mocked `convert()`)
- [x] 3.3 Test: invoking when `convert()` raises produces a non-zero exit code and an error message on stderr

## 4. HTTP API Adapter

- [x] 4.1 Implement `src/text2gherkin/adapters/api.py`: a FastAPI app with `POST /convert`, using Pydantic models for the `{"text": str}` request and `{"gherkin": str}` response
- [x] 4.2 Wire error handling: catch exceptions from `convert()` and return a 502 response with a `detail` field

## 5. API Tests

- [x] 5.1 Test: `POST /convert` with a valid body returns 200 and the expected `gherkin` field (mocked `convert()`, via FastAPI `TestClient`)
- [x] 5.2 Test: `POST /convert` when `convert()` raises returns 502 with a `detail` field (mocked `convert()`)
- [x] 5.3 Test: `POST /convert` with a missing `text` field returns 422

## 6. MCP Server Adapter

- [x] 6.1 Implement `src/text2gherkin/adapters/mcp_server.py`: a `FastMCP` server (from the `mcp` SDK) exposing `convert` as a tool
- [x] 6.2 Wire error handling: catch exceptions from `convert()` and return an MCP error result instead of letting the server crash — verified `FastMCP` does this automatically (no manual try/except needed): a tool raising surfaces as `CallToolResult(isError=True, ...)` to the client rather than crashing the server

## 7. MCP Smoke Test

- [x] 7.1 Parse the mocked `convert()` output with `gherkin-official` as part of test 7.2's assertions, confirming tool output is valid Gherkin before checking protocol behavior
- [x] 7.2 Write an in-process MCP client test (per design: SDK's own client/server session, no external agent needed): connect, list tools, confirm `convert` is present, then call it with valid input (mocked `convert()`) and confirm the result
- [x] 7.3 Write an in-process MCP client test: call `convert` with input that makes the (mocked) engine raise, and confirm the client receives an MCP error result rather than the connection crashing
