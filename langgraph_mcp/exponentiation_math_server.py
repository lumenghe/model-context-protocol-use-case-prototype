from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Exponentiation")


@mcp.tool()
def exponentiation(a: int, b: int) -> int:
    """Add two numbers"""
    return a**b


if __name__ == "__main__":
    mcp.run(transport="stdio")
