## 1. Dockerfile

- [x] 1.1 Create `.dockerignore` excluding `.venv/`, `.git/`, `__pycache__/`, `openspec/`, and `tests/`
- [x] 1.2 Write `Dockerfile`: single-stage build on `python:3.11-slim`, `pip install .` the project, `CMD` running uvicorn on `0.0.0.0:8000` serving `text2gherkin.adapters.api:app`
- [x] 1.3 Build the image locally (`docker build -t text2gherkin .`) and confirm it builds without errors — neither the local machine nor a remote sandbox had a working Docker daemon (local: Docker Desktop not running; remote: daemon returned HTTP 500 to every call), so verification was done instead via a GitHub Actions workflow (`.github/workflows/docker-verify.yml`) on an `ubuntu-latest` runner, which has a genuinely working Docker engine. Build step passed: [run](https://github.com/ibuprofano/ai4devs-openspec-sandbox-202606-sr-2/actions/runs/30028027502)

## 2. Verify the API Inside the Container

- [x] 2.1 Run the image with port mapping and no command override (`docker run -d -p 8000:8000 text2gherkin`), confirm the container starts and stays running — passed in CI
- [x] 2.2 Send a `POST /convert` request to the mapped port with a configured API key and confirm a 200 response with a `gherkin` field (or, if no key is available, confirm the request fails the same documented way it does locally without a key — not a crash) — no API key was configured in the CI runner; confirmed graceful 502 with a `detail` field, not a crash
- [x] 2.3 Stop and remove the test container — passed in CI

## 3. Verify the CLI Inside the Container

- [x] 3.1 Run the image with the command overridden to the CLI (`docker run --rm -i text2gherkin text2gherkin convert`), piping input text via stdin — passed in CI
- [x] 3.2 Confirm the CLI produces output on stdout inside the container the same way it does locally, and exits 0 on success — no API key configured in CI, so confirmed the documented failure path instead: clean non-zero exit, no raw Python traceback in output
- [x] 3.3 Confirm no API key or secret is present in the built image (`docker history` / inspecting layers) — nothing baked in beyond what's passed via `-e` at run time — confirmed via `docker history --no-trunc` and `docker inspect`, no secrets found
