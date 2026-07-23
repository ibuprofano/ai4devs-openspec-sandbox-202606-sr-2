import os

import litellm

DEFAULT_MODEL = "anthropic/claude-sonnet-5"


def call_llm(prompt: str) -> str:
    """Send a prompt to the configured LLM provider/model and return the raw text response."""
    model = os.environ.get("TEXT2GHERKIN_MODEL", DEFAULT_MODEL)
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
