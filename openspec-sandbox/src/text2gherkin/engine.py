from pathlib import Path

from text2gherkin.llm import call_llm
from text2gherkin.validate import validate_gherkin

_PROMPT_TEMPLATE_PATH = Path(__file__).parent / "prompts" / "convert_v1.md"
_MAX_ATTEMPTS = 3


def convert(text: str) -> str:
    """Convert free-form text describing user actions into a Gherkin feature document."""
    template = _PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    prompt = template.replace("{input_text}", text)

    last_error = None
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        if last_error is not None:
            prompt = (
                f"{prompt}\n\nYour previous attempt was not valid Gherkin. "
                f"Parser error:\n{last_error}\n\nFix the output and try again. "
                f"Output only the corrected Gherkin content."
            )

        candidate = call_llm(prompt)
        result = validate_gherkin(candidate)

        if result.valid:
            return candidate

        last_error = result.error

    raise ValueError(
        f"Failed to produce valid Gherkin after {_MAX_ATTEMPTS} attempts. "
        f"Last parser error: {last_error}"
    )
