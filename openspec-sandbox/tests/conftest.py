import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest


@pytest.fixture
def llm_api_key():
    """Skip the requesting test if no usable LLM API key is configured."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("no LLM API key configured")
