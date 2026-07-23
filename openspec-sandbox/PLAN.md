# Implementation Plan — Text → Gherkin Utility

Reference plan for implementing the utility described in `openspec/config.yaml`.
Each group below is intended to become one OpenSpec change (proposal + design +
spec deltas + tasks), with its sub-items as the checklist in that change's
`tasks.md`. Groups are ordered so no later group requires rework of an earlier one.

## Group 1: Core Engine Foundation
- TECH-01 — Scaffold Python package structure (`pyproject.toml`, src layout, pinned deps: LiteLLM, gherkin-official, Typer, FastAPI, pytest)
- TECH-02 — Define core `convert(text: str) -> str` function signature and module layout (engine vs. adapters), stubbed with a placeholder return
- TECH-03 — Add versioned prompt template file(s) with initial few-shot examples for NL → Gherkin translation
- TECH-04 — Implement LLM abstraction layer (LiteLLM wrapper) with provider/model configurable via env vars, defaulting to Claude Sonnet 5
- TECH-05 — Implement Gherkin validation layer using `gherkin-official` (parse candidate output, return valid/invalid + error detail)
- TECH-06 — Wire core `convert()`: call LLM abstraction with the prompt template, validate output, implement reject-and-retry on invalid Gherkin

## Group 2: Core Engine Verification
- TECH-07 — Create golden-file fixture set (3–5 representative input texts + expected `.feature` outputs)
- TECH-08 — Write pytest suite for `convert()` against golden fixtures, including a forced-invalid-output retry case

## Group 3: Integration Surfaces
- TECH-09 — Implement CLI (Typer) `convert` command wrapping the core function (stdin/file in, stdout/file out)
- TECH-10 — Write CLI tests (invocation, file I/O, exit codes)
- TECH-11 — Implement FastAPI `POST /convert` endpoint wrapping the core function
- TECH-12 — Write API tests (FastAPI TestClient, request/response schema validation)
- TECH-13 — Implement MCP server wrapper exposing `convert` as an MCP tool
- TECH-14 — Smoke-test the MCP wrapper against an MCP client (e.g. Claude Code)

## Group 4: Packaging
- TECH-15 — Write Dockerfile bundling CLI + API entrypoints
- TECH-16 — Verify Docker image: build, then confirm both CLI invocation and API endpoint work inside the container

## Group phase gates
- Group 1 → 2: the engine works end to end
- Group 2 → 3: the engine is proven correct (don't build adapters on an unverified core)
- Group 3 → 4: all integration surfaces exist and are tested
