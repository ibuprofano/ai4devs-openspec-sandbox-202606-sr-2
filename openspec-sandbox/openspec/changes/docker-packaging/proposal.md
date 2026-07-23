## Why

The CLI, HTTP API, and MCP server (built in `integration-surfaces`) currently only run from a local Python virtual environment with manually-installed dependencies. `openspec/config.yaml` calls for Docker packaging specifically so the utility is deployable without requiring a consumer to have Python, the right version, or the project's exact dependency set installed. This is the last piece needed to make the utility genuinely "integrable across different tech stacks and contexts" as originally scoped.

## What Changes

- Add a `Dockerfile` that installs the project and its dependencies into an image, bundling the CLI and the API
- The image's default entrypoint runs the API server (`uvicorn`, serving `text2gherkin.adapters.api:app`); the CLI remains reachable inside the same image via `docker run --rm <image> text2gherkin convert ...` (overriding the entrypoint), so one image serves both surfaces without needing two separate builds
- Verify the built image actually works: both the CLI invocation and the API endpoint respond correctly when run inside a container, not just when run locally

## Capabilities

### New Capabilities
- `docker-packaging`: the system is distributable as a single Docker image that bundles both the CLI and the API, runnable without a local Python installation

### Modified Capabilities
(none — packaging doesn't change what the CLI, API, MCP server, or conversion engine do; it only changes how they're deployed and run)

## Example Input → Expected Output

Same conversion behavior as already specified; this capability only changes how the software is packaged and launched, not what it does. Concretely:

```
$ docker build -t text2gherkin .
$ docker run -d -p 8000:8000 text2gherkin
$ curl -X POST localhost:8000/convert -H "content-type: application/json" \
    -d '{"text": "A logged-in user adds an item to their cart..."}'
-> {"gherkin": "Feature: Add item to cart\n..."}

$ docker run --rm -i text2gherkin text2gherkin convert < input.txt
Feature: Add item to cart
...
```

## Impact

- New file: `Dockerfile` at the project root (`openspec-sandbox/`)
- No changes to `src/text2gherkin/` — the engine, adapters, and their behavior are unchanged; this change only adds a way to run the existing code in a container
- No new persistent storage: the container is stateless, same as the application it packages; nothing is written to a volume or external store
- Requires Docker to be installed to build/run the image (build- and run-time only, not a Python dependency)
