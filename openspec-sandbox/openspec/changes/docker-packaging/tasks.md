## 1. Dockerfile

- [x] 1.1 Create `.dockerignore` excluding `.venv/`, `.git/`, `__pycache__/`, `openspec/`, and `tests/`
- [x] 1.2 Write `Dockerfile`: single-stage build on `python:3.11-slim`, `pip install .` the project, `CMD` running uvicorn on `0.0.0.0:8000` serving `text2gherkin.adapters.api:app`
- [ ] 1.3 Build the image locally (`docker build -t text2gherkin .`) and confirm it builds without errors

## 2. Verify the API Inside the Container

- [ ] 2.1 Run the image with port mapping and no command override (`docker run -d -p 8000:8000 text2gherkin`), confirm the container starts and stays running
- [ ] 2.2 Send a `POST /convert` request to the mapped port with a configured API key and confirm a 200 response with a `gherkin` field (or, if no key is available, confirm the request fails the same documented way it does locally without a key — not a crash)
- [ ] 2.3 Stop and remove the test container

## 3. Verify the CLI Inside the Container

- [ ] 3.1 Run the image with the command overridden to the CLI (`docker run --rm -i text2gherkin text2gherkin convert`), piping input text via stdin
- [ ] 3.2 Confirm the CLI produces output on stdout inside the container the same way it does locally, and exits 0 on success
- [ ] 3.3 Confirm no API key or secret is present in the built image (`docker history` / inspecting layers) — nothing baked in beyond what's passed via `-e` at run time
