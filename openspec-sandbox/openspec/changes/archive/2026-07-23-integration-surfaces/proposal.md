## Why

The `convert()` engine (built and verified in `core-engine-foundation` and `core-engine-verification`) is only usable by importing the Python package directly. `openspec/config.yaml` explicitly requires this utility to be "integrable across different tech stacks and contexts, not just consumed as a Python library" — a non-Python service, a CI pipeline script, or an AI agent/IDE can't call a Python function directly. This change adds the three integration surfaces the project plan always intended: a CLI, a REST API, and an MCP tool wrapper, so the engine is actually usable outside a Python codebase.

## What Changes

- Add a CLI (`text2gherkin convert`, via Typer) that reads input text from a file argument or stdin, calls `convert()`, and writes the result to an output file (`-o`) or stdout
- Add a REST API (`POST /convert`, via FastAPI) that accepts JSON `{"text": "..."}` and returns `{"gherkin": "..."}`, for services in any language to call over HTTP
- Add an MCP server wrapper exposing `convert` as a tool, so MCP-compatible agents and IDEs (e.g. Claude Code) can invoke it directly
- All three are thin adapters over the existing `convert()` function (per `core-engine-foundation`'s design) — none of them re-implement conversion, validation, or retry logic

## Capabilities

### New Capabilities
- `cli-interface`: a command-line tool that converts text to Gherkin via file or stdin/stdout, for use in shells and CI pipelines regardless of the caller's language
- `http-api`: a REST endpoint that converts text to Gherkin over HTTP, for non-Python services to call
- `mcp-server`: an MCP tool that converts text to Gherkin, for agents and IDEs that speak MCP

### Modified Capabilities
(none — `gherkin-conversion`'s behavior is unchanged; these are new ways to invoke the existing engine, not changes to how it converts text)

## Example Input → Expected Output

Same conversion behavior as already specified for `gherkin-conversion`; these capabilities only change how the input/output travels, not what it looks like. For a concrete request/response example:

**HTTP API:**
```
POST /convert
{"text": "A logged-in user adds an item to their cart. If the item is out of stock, they should see an error message instead and the cart should not change."}

-> 200 OK
{"gherkin": "Feature: Add item to cart\n\n  Scenario: Adding an in-stock item...\n"}
```

**CLI:**
```
$ text2gherkin convert input.txt -o output.feature
$ cat output.feature
Feature: Add item to cart
...
```

## Impact

- New modules: `src/text2gherkin/adapters/cli.py`, `src/text2gherkin/adapters/api.py`, `src/text2gherkin/adapters/mcp_server.py` (the `adapters/` package was reserved for exactly this in `core-engine-foundation`)
- New dependencies: `mcp` (official Python MCP SDK, verified available on PyPI at v1.28.1) in addition to the already-pinned Typer and FastAPI
- No persistent storage: all three adapters are stateless request/response wrappers around `convert()`; no new DB, no session state, no request history
- No change to `src/text2gherkin/engine.py`, `llm.py`, `validate.py`, or the prompt template
