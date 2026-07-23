from dataclasses import dataclass

from gherkin.parser import Parser


@dataclass
class ValidationResult:
    valid: bool
    error: str | None = None


def validate_gherkin(text: str) -> ValidationResult:
    """Parse candidate text against the official Gherkin grammar."""
    try:
        Parser().parse(text)
        return ValidationResult(valid=True)
    except Exception as exc:
        return ValidationResult(valid=False, error=str(exc))
