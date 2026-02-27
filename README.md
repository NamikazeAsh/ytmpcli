# ytmpcli

Minimalist YT downloader. Built for personal use.

Extracts native audio (M4A) and video (MP4). Fast, clean, no fluff.

## Features

- **Interactive**: Paste links in a loop.
- **Auto-Sort**: Playlists automatically go into folders.
- **Bulk**: Feed it a `.txt` file with one link per line.
- **Native Quality**: Grabs the best source (M4A).
- **Global**: All downloads go to `Downloads/ytmpcli`.

## Installation

1. **FFmpeg**: Required for media processing. Download and add to PATH.
2. **Setup**:
   ```bash
   git clone https://github.com/NamikazeAsh/ytmpcli.git
   cd ytmpcli
   pip install -e .
   ```

## Usage

Run `ytmpcli`.

### Commands

- `[link]` : Paste any YT link.
- `s:<query>` : Search & download top result.
- `audio` / `video` : Toggle mode.
- `res` : Change video res.
- `open` : Open the folder.
- `?` : Help menu.
- `q` : Exit.

---

Uses **yt-dlp**. Built for a faster workflow when building local collections (like mine!).

Created by **NamikazeAsh**
