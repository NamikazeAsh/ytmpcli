import yt_dlp
import os

class MyLogger:
    def debug(self, msg):
        if msg.startswith('[debug] ') or msg.startswith('[youtube] '):
            pass
        else:
            self.info(msg)
    def info(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(f"Error: {msg}")

def progress_hook(d):
    if d['status'] == 'downloading':
        info = d.get('info_dict', {})
        idx = info.get('playlist_index')
        total = info.get('n_entries')
        title = info.get('title', 'Unknown')
        
        counter = f"[{idx}/{total}] " if idx and total else ""
        display_title = (title[:40] + '..') if len(title) > 40 else title
        
        p = d.get('_percent_str', ' 0%').replace('%','')
        try:
            percent = float(p)
        except:
            percent = 0
        
        width = 20
        filled = int(width * percent / 100)
        bar = '█' * filled + '░' * (width - filled)
        
        if not hasattr(progress_hook, 'current_title') or progress_hook.current_title != title:
            print(f"\n  {counter}{display_title}")
            progress_hook.current_title = title

        print(f"\r  {bar} {percent:.1f}%", end='', flush=True)
    elif d['status'] == 'finished':
        width = 20
        bar = '█' * width
        if d.get('total_bytes') is None and d.get('downloaded_bytes') is None:
             print(f"\r  {bar} 100% (exists) ✓")
        else:
             print(f"\r  {bar} 100% ✓")

def download_media(url, is_playlist=False, file_format='audio', quality='best', output_path=None):
    if output_path is None:
        home = os.path.expanduser("~")
        output_path = os.path.join(home, "Downloads", "ytmpcli")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': not is_playlist,
        'quiet': True,
        'no_warnings': True,
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
        'nooverwrites': True,
        'restrictfilenames': True,
    }

    if file_format == 'audio':
        # Best native audio stream (usually m4a or opus)
        ydl_opts.update({
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a', # Ensures high compatibility
            }],
        })
    else:
        # Best native MP4 video
        f_str = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best'
        if quality == 'best': f_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts.update({'format': f_str})

    if is_playlist:
        ydl_opts['outtmpl'] = os.path.join(output_path, '%(playlist_title)s', '%(title)s.%(ext)s')

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if "/@" in url or "/channel/" in url or "/c/" in url:
                print(f"  ✗ error » channels not supported")
                return
            info = ydl.extract_info(url, download=False, process=False)
            title = info.get('title', 'Unknown')
            if info.get('_type') == 'playlist' or 'entries' in info:
                print(f"\n  playlist » {title}")
                print(f"  path     » ./{title}/")
            if hasattr(progress_hook, 'current_title'):
                delattr(progress_hook, 'current_title')
            ydl.params['process'] = True
            ydl.download([url])
    except Exception as e:
        err_msg = str(e)
        if "Unsupported URL" in err_msg: print(f"  ✗ error » unsupported link")
        elif "video is unavailable" in err_msg.lower(): print(f"  ✗ error » video unavailable")
        else: print(f"  ✗ error » download failed")

def smart_download(url, file_format='audio', quality='best'):
    is_playlist = "list=" in url
    download_media(url, is_playlist=is_playlist, file_format=file_format, quality=quality)
