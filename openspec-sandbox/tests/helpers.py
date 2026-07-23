from gherkin.parser import Parser

from text2gherkin.validate import validate_gherkin


def _scenario_step_counts(gherkin_text: str) -> list[int]:
    document = Parser().parse(gherkin_text)
    counts = []
    for child in document["feature"]["children"]:
        scenario = child.get("scenario")
        if scenario is None:
            continue
        counts.append(len(scenario["steps"]))
    return counts


def assert_structurally_equivalent(actual: str, expected: str) -> None:
    """Assert two Gherkin documents both parse as valid Gherkin and have the
    same number of scenarios with the same step count per scenario, in order.
    Does not require exact step wording or scenario titles to match, since
    LLM output isn't byte-identical across runs (title phrasing especially
    varies freely while describing the same behavior).
    """
    actual_result = validate_gherkin(actual)
    assert actual_result.valid, f"Actual output was not valid Gherkin: {actual_result.error}"

    expected_result = validate_gherkin(expected)
    assert expected_result.valid, f"Expected fixture was not valid Gherkin: {expected_result.error}"

    actual_counts = _scenario_step_counts(actual)
    expected_counts = _scenario_step_counts(expected)
    assert actual_counts == expected_counts, (
        f"Scenario structure mismatch (step counts per scenario).\n"
        f"Actual:   {actual_counts}\nExpected: {expected_counts}"
    )
