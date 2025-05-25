from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Elementary")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


@mcp.tool()
def subtraction(a: int, b: int) -> int:
    """Add two numbers"""
    return a - b


@mcp.tool()
def division(a: int, b: int) -> tuple[int, int]:
    """Multiply two numbers"""
    return a // b, a % b


if __name__ == "__main__":
    mcp.run(transport="stdio")
