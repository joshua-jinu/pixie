from langchain_core.tools import tool

@tool
async def summarize(url: str) -> str:
    """Summarizes the content of a web page given its URL."""
    return f"Summarized content of {url}"

@tool
async def spotify_controller(action: str, **kwargs) -> str:
    """Controls Spotify playback. Action can be 'play', 'pause', or 'next'."""
    if action == "play":
        return "Spotify playback started."
    elif action == "pause":
        return "Spotify playback paused."
    elif action == "next":
        return "Skipped to the next track on Spotify."
    else:
        return f"Unknown Spotify action: {action}"