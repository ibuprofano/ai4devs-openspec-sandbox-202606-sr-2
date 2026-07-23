# text2gherkin

Converts free-form text describing user actions (requirements, user stories, meeting notes, manual QA scripts, chat transcripts) into valid BDD/Gherkin `.feature` files.

The conversion logic lives in one place (`text2gherkin.engine.convert`) and is exposed through three interfaces: a CLI, an HTTP API, and an MCP tool. Pick whichever fits your context — none of them require the others.

## Setup

Requires Python 3.11+.

```bash
pip install -e .
```

This installs the package (making `text2gherkin.*` importable) and registers the `text2gherkin` CLI command.

### Configuration

| Variable | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes, for the default model | Anthropic API key with available credits (console.anthropic.com → Plans & Billing) |
| `TEXT2GHERKIN_MODEL` | No | Overrides the default model. Accepts any [LiteLLM](https://docs.litellm.ai/docs/providers) model string, e.g. `openai/gpt-4o`, if you'd rather use a different provider — set the matching provider's API key env var instead of `ANTHROPIC_API_KEY` in that case. |

Without a working key, all three interfaces still run — conversion requests just fail with a clear error instead of a crash (this is by design; see `openspec/specs/gherkin-conversion/spec.md`).

## 1. CLI

```bash
text2gherkin convert INPUT_FILE [-o OUTPUT_FILE]
```

- `INPUT_FILE` is optional — omit it to read from stdin
- `-o OUTPUT_FILE` is optional — omit it to write to stdout
- On failure, prints an error to stderr and exits non-zero

**Examples:**

```bash
# file to file
text2gherkin convert input.txt -o output.feature

# pipe to pipe
cat input.txt | text2gherkin convert > output.feature

# quick one-off
echo "A logged-in user adds an item to their cart. If the item is out of stock, they should see an error message instead and the cart should not change." | text2gherkin convert
```

## 2. HTTP API

Run it locally with uvicorn:

```bash
uvicorn text2gherkin.adapters.api:app --host 0.0.0.0 --port 8000
```

**Endpoint:** `POST /convert`

| | |
|---|---|
| Request body | `{"text": "<free-form text>"}` |
| 200 response | `{"gherkin": "<converted feature text>"}` |
| 502 response | `{"detail": "<error message>"}` — conversion failed (e.g. no API key, or the model couldn't produce valid Gherkin after retries) |
| 422 response | request body was missing/malformed `text` |

**Example:**

```bash
curl -X POST http://localhost:8000/convert \
  -H "content-type: application/json" \
  -d '{"text": "A logged-in user adds an item to their cart. If the item is out of stock, they should see an error message instead and the cart should not change."}'
```

## 3. MCP Server

Runs over stdio, for MCP-compatible clients (Claude Code, Claude Desktop, other MCP agents/IDEs) to launch as a subprocess:

```bash
python -m text2gherkin.adapters.mcp_server
```

Register it with your MCP client using its stdio-server config format. The common shape across clients:

```json
{
  "mcpServers": {
    "text2gherkin": {
      "command": "python",
      "args": ["-m", "text2gherkin.adapters.mcp_server"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-..."
      }
    }
  }
}
```

Where this goes depends on the client — e.g. Claude Desktop's `claude_desktop_config.json`, or Claude Code's `claude mcp add` command / project `.mcp.json`. Consult your client's docs for the exact file/command.

Once connected, the client can call the `convert` tool with a `text` argument and receive the Gherkin output as the result.

## Docker (bundles the CLI + API)

One image serves both surfaces — the MCP server isn't containerized, since it's meant to run as a local subprocess alongside its client rather than as a standalone service (see `openspec/specs/docker-packaging/spec.md` for what is packaged).

```bash
docker build -t text2gherkin .
```

**Run the API** (default command):

```bash
docker run -d -p 8000:8000 -e ANTHROPIC_API_KEY=sk-ant-... text2gherkin
curl -X POST localhost:8000/convert -H "content-type: application/json" \
  -d '{"text": "..."}'
```

**Run the CLI** (override the container's command):

```bash
echo "some input text" | docker run --rm -i -e ANTHROPIC_API_KEY=sk-ant-... text2gherkin text2gherkin convert
```

No API key is ever baked into the image — pass it at `docker run` time with `-e`, as shown above.
