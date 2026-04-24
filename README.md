# ytmpcli

Minimalist YT downloader. Built for personal use.

Extracts native audio (M4A) and video (MP4). Fast, clean, no fluff.

## Features

- **Interactive**: Paste links in a loop.
- **Auto-Sort**: Playlists automatically go into folders.
- **Bulk**: Feed it a `.txt` file with one link per line.
- **Native Quality**: Grabs the best source (M4A).
- **Rename**: Optionally set a custom filename after each download.
- **Global**: All downloads go to `Downloads/ytmpcli`.

## Installation

**Option 1 — Standalone exe (no Python needed):**
Download `ytmpcli.exe` from the [releases page](https://github.com/NamikazeAsh/ytmpcli/releases/latest) and run it.

**Option 2 — pip:**
```bash
pip install git+https://github.com/NamikazeAsh/ytmpcli.git
```

**Dev install:**
```bash
git clone https://github.com/NamikazeAsh/ytmpcli.git
cd ytmpcli
pip install -e .
```

## Usage

Run `ytmpcli`.

- `[link]` : Paste any YT link.
- `s:<query>` : Search & download top result.
- `s3:<query>` / `s5:<query>` : Search & pick from 3 or 5 results.
- `audio` / `video` : Toggle mode.
- `res` : Change video res.
- `rename` : Toggle custom filename prompt after download.
- `update` : Check for updates and upgrade.
- `open` : Open the folder.
- `?` : Help menu.
- `q` : Exit.

---

Uses **yt-dlp**. Created by **NamikazeAsh**.
