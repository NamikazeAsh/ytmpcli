import argparse
import sys
import re
from .downloader import download_media, smart_download, fetch_search_results
import os

def _do_update():
    import urllib.request, json, subprocess
    try:
        print("  checking for updates...")
        req = urllib.request.Request(
            "https://api.github.com/repos/NamikazeAsh/ytmpcli/tags",
            headers={"Accept": "application/vnd.github+json"}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            tags = json.loads(r.read())
        if not tags:
            print("  ✗ no releases found")
            return
        latest = tags[0]['name'].lstrip('v')
        from ytmpcli import __version__ as current
        print(f"  current: {current}  →  latest: {latest}")
        if latest == current:
            print("  already up to date ✓")
            return
        if getattr(sys, 'frozen', False):
            print("  download the new version at:")
            print("  github.com/NamikazeAsh/ytmpcli/releases/latest")
        else:
            print("  updating...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade",
                 "git+https://github.com/NamikazeAsh/ytmpcli.git"],
                check=True, capture_output=True
            )
            print("  done ✓  restart ytmpcli to use the new version")
    except Exception as e:
        print(f"  ✗ update failed: {e}")

def _format_duration(seconds):
    if not seconds:
        return '?:??'
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def _rename_file(filepath):
    new_name = input("  name > ").strip()
    if not new_name:
        return
    ext = os.path.splitext(filepath)[1]
    new_path = os.path.join(os.path.dirname(filepath), new_name + ext)
    try:
        os.rename(filepath, new_path)
        print(f"  saved as » {new_name}{ext}")
    except Exception:
        print(f"  ✗ error » rename failed")

def _check_update_notify(current):
    def _check():
        try:
            import urllib.request, json
            req = urllib.request.Request(
                "https://api.github.com/repos/NamikazeAsh/ytmpcli/tags",
                headers={"Accept": "application/vnd.github+json"}
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                tags = json.loads(r.read())
            if tags:
                latest = tags[0]["name"].lstrip("v")
                if latest != current:
                    print(f"  update available: v{latest}  ->  type [update] to upgrade")
        except Exception:
            pass
    import threading
    threading.Thread(target=_check, daemon=True).start()

def interactive_mode():
    os.system('cls' if os.name == 'nt' else 'clear')
    home = os.path.expanduser("~")
    target = os.path.join(home, "Downloads", "ytmpcli")
    
    fmt = "audio"
    q_video = "1080"
    rename = False
    
    from ytmpcli import __version__
    header = f"""
    █▄█ ▀█▀ █▀▄▀█ █▀█ █▀▀ █   █
    ░█░ ░█░ █░▀░█ █▀▀ █▄▄ █▄▄ █
    
    by NamikazeAsh - v{__version__}
    """
    print(header)
    print(f"  ready  » {target}")
    print(f"  inputs » [link], [audio/video], [res], [?], or [q]uit")
    print("  " + "─" * 55)
    _check_update_notify(__version__)

    while True:
        try:
            curr_mode = "audio" if fmt == "audio" else f"video:{q_video}p"
            rename_tag = " +rename" if rename else ""
            prompt = f"\n  link ({curr_mode}{rename_tag}) > "
            url = input(prompt).strip()
            
            if not url: continue
            if url.lower() in ['exit', 'quit', 'q']: break
            
            if url == '?':
                print("\n  [ commands ]")
                print("  audio, video : switch mode")
                print("  res          : change video res")
                print("  rename       : toggle custom filename prompt")
                print("  s:<query>    : search & download top result")
                print("  s3:<query>   : search & pick from 3 results")
                print("  s5:<query>   : search & pick from 5 results")
                print("  update       : check for updates and upgrade")
                print("  open         : open downloads folder")
                print("  <name>.txt   : bulk download from file")
                print("  q            : exit")
                continue

            if url.lower() == 'update':
                _do_update()
                continue

            if url.lower() == 'open':
                if not os.path.exists(target): os.makedirs(target)
                os.startfile(target)
                print("  opening folder...")
                continue

            m = re.match(r'^s(\d*):', url, re.IGNORECASE)
            if m:
                count = int(m.group(1)) if m.group(1) else 1
                query = url[m.end():].strip()
                if not query: continue
                print(f"  searching: {query}")
                if count <= 1:
                    files = smart_download(f"ytsearch1:{query}", file_format=fmt,
                                           quality='best' if fmt == "audio" else q_video)
                else:
                    results = fetch_search_results(query, count)
                    if not results:
                        print("  ✗ no results")
                        continue
                    for i, r in enumerate(results, 1):
                        t = (r['title'][:50] + '..') if len(r['title']) > 50 else r['title']
                        print(f"  {i}. {t} [{_format_duration(r['duration'])}]")
                    sel = input(f"  pick [1-{len(results)}] or enter to cancel > ").strip()
                    if not sel or not sel.isdigit() or not (1 <= int(sel) <= len(results)):
                        continue
                    chosen = results[int(sel) - 1]
                    files = smart_download(f"https://www.youtube.com/watch?v={chosen['id']}",
                                           file_format=fmt, quality='best' if fmt == "audio" else q_video)
                if rename and len(files) == 1:
                    _rename_file(files[0])
                continue

            if url.lower() == 'rename':
                rename = not rename
                print(f"  rename {'on' if rename else 'off'}")
                continue

            if url.lower() == 'audio':
                fmt = "audio"
                print(f"  switched to audio mode (high quality)")
                continue
            if url.lower() == 'video':
                fmt = "video"
                print(f"  switched to video mode (MP4)")
                continue
            
            if url.lower() == 'res' and fmt == 'video':
                print("  1: 480p | 2: 720p | 3: 1080p | 4: best")
                sel = input("  select [1-4] > ").strip()
                opts = {"1":"480", "2":"720", "3":"1080", "4":"best"}
                if sel in opts:
                    q_video = opts[sel]
                    print(f"  res set to {q_video}p")
                continue
            
            if url.lower().endswith('.txt'):
                if os.path.exists(url):
                    with open(url, 'r') as f:
                        links = [line.strip() for line in f if line.strip()]
                    print(f"  found {len(links)} links in {url}")
                    for i, link in enumerate(links):
                        print(f"  item {i+1}/{len(links)}")
                        smart_download(link, file_format=fmt, quality='best' if fmt == "audio" else q_video)
                else:
                    print(f"  ✗ error » file not found")
                continue
            
            files = smart_download(url, file_format=fmt, quality='best' if fmt == "audio" else q_video)
            if rename and len(files) == 1:
                _rename_file(files[0])
            print("")
        except KeyboardInterrupt:
            print("\nbye.")
            break
        except Exception as e:
            print(f"  !")

def main():
    parser = argparse.ArgumentParser(description="ytmpcli: A simple YouTube downloader for High-Quality Media.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--n", metavar="URL", help="Download a single video (normal)")
    group.add_argument("--p", metavar="URL", help="Download an entire playlist")
    parser.add_argument("-f", "--format", choices=["audio", "video"], default="audio", help="Output format")

    if len(sys.argv) == 1:
        interactive_mode()
        return

    args = parser.parse_args()
    if args.n or args.p:
        url = args.n or args.p
        is_playlist = bool(args.p)
        print(f"Initiating download in {args.format.upper()} mode...")
        download_media(url, is_playlist=is_playlist, file_format=args.format)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
