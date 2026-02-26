# ytmpcli

> Minimalist YT downloader. Built for personal use, now public.

Organizes playlists into folders, embeds cover art, and handles MP3/MP4 on the fly. Fast, clean, and zero fluff.

## Features
- **Interactive Loop**: Paste links back-to-back without restarting.
- **Auto-Playlist**: Automatically creates folders for playlists.
- **Global Saving**: All downloads centralize in `Downloads/ytmpcli`.
- **Dynamic Quality**: Toggle bitrates (128k-320k) and resolution (480p-1080p) on the fly.
- **Auto-Tagging**: Automatically embeds high-res cover art and metadata tags.
- **No Duplicates**: Skips existing files instantly.

## Installation

1. **Ensure FFmpeg is installed** (Required for metadata and MP3 extraction).
2. **Setup**:
   ```bash
   git clone https://github.com/NamikazeAsh/ytmpcli.git
   cd ytmpcli
   pip install -e .
   ```

## Usage

Run the tool from any terminal:
```bash
ytmpcli
```

### In-App Commands
- `[link]` : Paste any YT link to start.
- `mp4` / `mp3` : Toggle between video and audio mode.
- `bitrate` : Change MP3 quality (128k - 320k).
- `res` : Change MP4 resolution (480p - 1080p).
- `q` : Exit.

## Structure
- `ytmpcli/cli.py` : CLI & interactive logic.
- `ytmpcli/downloader.py` : Download engine.
- `setup.py` : Entry point configuration.

---
Created by **NamikazeAsh**
