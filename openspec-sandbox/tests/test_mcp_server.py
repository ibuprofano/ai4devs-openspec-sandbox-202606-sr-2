import asyncio
from unittest.mock import patch

from mcp.shared.memory import create_connected_server_and_client_session

from text2gherkin.adapters.mcp_server import mcp
from text2gherkin.validate import validate_gherkin

VALID_GHERKIN = "Feature: X\n\n  Scenario: Y\n    Given a\n    When b\n    Then c\n"


def test_convert_tool_is_discoverable():
    async def run():
        async with create_connected_server_and_client_session(mcp._mcp_server) as client:
            tools = await client.list_tools()
            assert "convert" in [t.name for t in tools.tools]

    asyncio.run(run())


def test_convert_tool_call_with_valid_input():
    async def run():
        with patch("text2gherkin.adapters.mcp_server._convert", return_value=VALID_GHERKIN):
            async with create_connected_server_and_client_session(mcp._mcp_server) as client:
                result = await client.call_tool("convert", {"text": "some input"})

        assert result.isError is False
        output_text = result.content[0].text

        validation = validate_gherkin(output_text)
        assert validation.valid, f"Tool output was not valid Gherkin: {validation.error}"
        assert output_text == VALID_GHERKIN

    asyncio.run(run())


def test_convert_tool_call_with_failing_input_returns_error_result():
    async def run():
        with patch("text2gherkin.adapters.mcp_server._convert", side_effect=ValueError("boom")):
            async with create_connected_server_and_client_session(mcp._mcp_server) as client:
                result = await client.call_tool("convert", {"text": "some input"})

        assert result.isError is True

    asyncio.run(run())
