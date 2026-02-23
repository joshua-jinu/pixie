from langchain_core.tools import tool

@tool
async def summarize(url: str) -> str:
    """Summarizes the content of a web page given its URL."""
    return f"Summarized content of {url}"