from pathlib import Path

import pytest

from helpers import assert_structurally_equivalent
from text2gherkin.engine import convert

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURE_NAMES = sorted(p.name for p in FIXTURES_DIR.iterdir() if p.is_dir())


@pytest.mark.parametrize("fixture_name", FIXTURE_NAMES)
def test_convert_matches_golden_fixture(fixture_name, llm_api_key):
    fixture_dir = FIXTURES_DIR / fixture_name
    input_text = (fixture_dir / "input.txt").read_text(encoding="utf-8")
    expected_output = (fixture_dir / "expected.feature").read_text(encoding="utf-8")

    actual_output = convert(input_text)

    assert_structurally_equivalent(actual_output, expected_output)
