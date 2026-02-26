from setuptools import setup, find_packages

setup(
    name="ytmpcli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
    ],
    entry_points={
        "console_scripts": [
            "ytmpcli=ytmpcli.cli:main",
            "ytmpcli-gui=ytmpcli.gui:main",
        ],
    },
    author="Ashwin",
    description="A simple CLI tool to download YouTube videos and playlists as MP3/MP4",
    python_requires=">=3.7",
)
