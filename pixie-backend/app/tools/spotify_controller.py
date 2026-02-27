import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from langchain_core.tools import tool

def get_spotify_client():
    scope = (
        "user-modify-playback-state "
        "user-read-playback-state "
        "user-read-currently-playing"
    )

    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=scope,
        cache_path=".spotify_cache",
        open_browser=True,
    )

    return spotipy.Spotify(auth_manager=auth_manager)

@tool
async def spotify_controller(command: str) -> str:
    """
    Control Spotify playback.

    Supported:
    - play <song name>
    - pause
    - next
    """

    sp = get_spotify_client()

    command = command.lower().strip()

    try:
        if command.startswith("play"):
            song = command.replace("play", "").strip()

            if not song:
                sp.start_playback()
                return "Resumed playback."

            results = sp.search(q=song, type="track", limit=1)

            if not results["tracks"]["items"]:
                return "Song not found."

            track = results["tracks"]["items"][0]
            sp.start_playback(uris=[track["uri"]])

            return f"Playing {track['name']} by {track['artists'][0]['name']}."

        elif command == "pause":
            sp.pause_playback()
            return "Playback paused."

        elif command == "next":
            sp.next_track()
            return "Skipped to next track."

        return "Unsupported Spotify command."

    except Exception as e:
        return f"Spotify error: {str(e)}"