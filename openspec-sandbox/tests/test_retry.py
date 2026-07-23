from unittest.mock import patch

import pytest

from text2gherkin import engine

VALID_GHERKIN = "Feature: X\n\n  Scenario: Y\n    Given a\n    When b\n    Then c\n"
INVALID_GHERKIN = "this is not gherkin at all"


def test_convert_retries_once_after_invalid_output():
    with patch.object(engine, "call_llm", side_effect=[INVALID_GHERKIN, VALID_GHERKIN]) as mock_call:
        result = engine.convert("some input")

    assert mock_call.call_count == 2
    assert result == VALID_GHERKIN

    second_call_prompt = mock_call.call_args_list[1].args[0]
    assert "previous attempt was not valid" in second_call_prompt


def test_convert_raises_after_exhausted_retries():
    with patch.object(engine, "call_llm", return_value=INVALID_GHERKIN) as mock_call:
        with pytest.raises(ValueError) as exc_info:
            engine.convert("some input")

    assert mock_call.call_count == engine._MAX_ATTEMPTS
    assert "Parser errors" in str(exc_info.value)
