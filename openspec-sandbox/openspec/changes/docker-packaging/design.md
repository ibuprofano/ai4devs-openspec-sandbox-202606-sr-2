## Context

Everything needed already exists: `pyproject.toml` declares all dependencies, the CLI has a console-script entry point (`text2gherkin`), and the API is a standard FastAPI `app` object servable by `uvicorn`. This change adds only packaging around existing, unchanged code.

## Goals / Non-Goals

**Goals:**
- One Docker image that can run either the API (as a long-lived server) or the CLI (as a one-off command), without building two separate images
- No source code changes required to achieve this — the image only installs and runs what already exists
- Verify the built image actually works end-to-end (both surfaces), not just that it builds

**Non-Goals:**
- Multi-stage build optimization for minimal image size — this is a sandbox/demo project (per the repo's own README), not a production deployment; a straightforward single-stage build is easier to read and verify, and image size isn't a stated constraint anywhere in `config.yaml`
- MCP server containerization — the MCP server communicates over stdio with a client process on the same machine (per `integration-surfaces`), which doesn't fit the same "expose a port" packaging model as the API; containerizing it is a reasonable future change but not part of this one
- Any change to `src/text2gherkin/` — this is packaging only

## Decisions

**1. Single-stage build on `python:3.11-slim`**
Alternative considered: multi-stage build (a builder stage installing dependencies, a slim final stage copying only the installed packages).
Chosen: single-stage. Multi-stage buys smaller image size at the cost of a more complex Dockerfile to read and debug, and nothing in this project's scope calls for minimizing image size. `python:3.11-slim` matches the pinned Python 3.11 from `config.yaml` and is already reasonably small.

**2. No fixed `ENTRYPOINT`; `CMD` defaults to running the API, fully overridable for the CLI**
Chosen: `CMD ["uvicorn", "text2gherkin.adapters.api:app", "--host", "0.0.0.0", "--port", "8000"]` with no `ENTRYPOINT`. Running the container with no arguments starts the API server. Running it with `docker run <image> text2gherkin convert ...` replaces `CMD` entirely and runs the CLI instead. This satisfies the proposal's "one image, both surfaces" goal without any wrapper script — plain Docker `CMD`-override semantics are enough.

**3. API binds to `0.0.0.0`, not `127.0.0.1`**
Chosen: explicit `--host 0.0.0.0` in the `CMD`. Uvicorn's own default is `127.0.0.1`, which is unreachable from outside the container even with `-p` port mapping. This is a necessary correction, not an architectural choice — the API adapter's own code doesn't set a host, so this must be supplied at the container's invocation layer.

**4. API keys are never baked into the image; passed at `docker run` time**
Chosen: no `ARG`/`ENV` for `ANTHROPIC_API_KEY` (or any provider key) in the Dockerfile. A container run without `-e ANTHROPIC_API_KEY=...` (or equivalent) will build and start fine, but conversion requests will fail exactly as they would locally without a key (per `core-engine-foundation`'s design, this is expected, not a bug to fix here). Baking a key into an image would leak it into every layer's history and anyone who pulls the image.

**5. Add a `.dockerignore`**
Chosen: exclude `.venv/`, `.git/`, `__pycache__/`, `openspec/`, and `tests/` from the build context. None of these are needed inside the image (the project is installed fresh via `pip install .` in the Dockerfile, not by copying a host virtualenv), and excluding them keeps the build context small and avoids accidentally shipping local dev artifacts.

## Risks / Trade-offs

- [Single-stage build produces a larger image than a multi-stage one would] → Accepted trade-off, per Non-Goals: this project has no stated size/production constraint, and a simpler Dockerfile is easier to verify correctly in one pass.
- [MCP server isn't containerized] → Accepted trade-off, per Non-Goals: its stdio-based, same-machine-client model doesn't fit the "run as a server, hit it from outside" pattern the API and CLI already do; revisit if a real need for a containerized MCP transport (e.g. over HTTP/SSE) arises.
- [Forgetting `--host 0.0.0.0` would make the API silently unreachable from outside the container] → Mitigated by baking the correct host into the image's default `CMD` (Decision 3), so the common case (`docker run -p 8000:8000 <image>`) works without the caller needing to know this detail.

## Migration Plan

Not applicable — this adds a new, optional way to run existing code. Nothing existing is deprecated or replaced; local development without Docker continues to work exactly as before.

## Open Questions

None outstanding — the build strategy, entrypoint behavior, networking, and secret handling are settled by the decisions above.
