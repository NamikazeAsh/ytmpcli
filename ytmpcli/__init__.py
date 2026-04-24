try:
    from importlib.metadata import version
    __version__ = version("ytmpcli")
except Exception:
    __version__ = "unknown"
