from mcp.server.fastmcp import FastMCP

from text2gherkin.engine import convert as _convert

mcp = FastMCP(name="text2gherkin")


@mcp.tool()
def convert(text: str) -> str:
    """Convert free-form text describing user actions into a Gherkin feature document."""
    return _convert(text)


if __name__ == "__main__":
    mcp.run()
