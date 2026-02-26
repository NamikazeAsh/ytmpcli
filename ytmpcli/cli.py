import argparse
import sys
from .downloader import download_media, smart_download
import os

def interactive_mode():
    os.system('cls' if os.name == 'nt' else 'clear')
    home = os.path.expanduser("~")
    target = os.path.join(home, "Downloads", "ytmpcli")
    
    fmt = "mp3"
    q_mp3 = "192"
    q_mp4 = "1080"
    
    header = """
    █▄█ ▀█▀ █▀▄▀█ █▀█ █▀▀ █   █
    ░█░ ░█░ █░▀░█ █▀▀ █▄▄ █▄▄ █
    
    by NamikazeAsh
    """
    print(header)
    print(f"  ready  » {target}")
    print(f"  inputs » [link], [s:<query>], [?], or [q]uit")
    print("  " + "─" * 55)

    while True:
        try:
            curr_q = q_mp3 if fmt == "mp3" else q_mp4
            prompt = f"\n  link ({fmt}:{curr_q}) > "
            url = input(prompt).strip()
            
            if not url: continue
            if url.lower() in ['exit', 'quit', 'q']: break
            
            if url == '?':
                print("\n  [ commands ]")
                print("  mp3, mp4     : switch format")
                print("  bitrate, res : change quality")
                print("  s:<query>     : search & download top result")
                print("  open         : open downloads folder")
                print("  <name>.txt   : bulk download from file")
                print("  q            : exit")
                continue

            if url.lower() == 'open':
                if not os.path.exists(target): os.makedirs(target)
                os.startfile(target)
                print("  opening folder...")
                continue

            if url.lower().startswith('s:'):
                query = url[2:].strip()
                if not query: continue
                print(f"  searching: {query}")
                search_url = f"ytsearch1:{query}"
                smart_download(search_url, file_format=fmt, quality=q_mp3 if fmt == "mp3" else q_mp4)
                continue

            if url.lower() == 'mp3':
                fmt = "mp3"
                print(f"  switched to {fmt}")
                continue
            if url.lower() == 'mp4':
                fmt = "mp4"
                print(f"  switched to {fmt}")
                continue
            
            if url.lower() == 'bitrate' and fmt == 'mp3':
                print("  1: 128k | 2: 192k | 3: 256k | 4: 320k")
                sel = input("  select [1-4] > ").strip()
                opts = {"1":"128", "2":"192", "3":"256", "4":"320"}
                if sel in opts:
                    q_mp3 = opts[sel]
                    print(f"  bitrate set to {q_mp3}k")
                continue

            if url.lower() == 'res' and fmt == 'mp4':
                print("  1: 480p | 2: 720p | 3: 1080p | 4: best")
                sel = input("  select [1-4] > ").strip()
                opts = {"1":"480", "2":"720", "3":"1080", "4":"best"}
                if sel in opts:
                    q_mp4 = opts[sel]
                    print(f"  res set to {q_mp4}p")
                continue
            
            if url.lower().endswith('.txt'):
                if os.path.exists(url):
                    with open(url, 'r') as f:
                        links = [line.strip() for line in f if line.strip()]
                    print(f"  found {len(links)} links in {url}")
                    for i, link in enumerate(links):
                        print(f"  item {i+1}/{len(links)}")
                        smart_download(link, file_format=fmt, quality=q_mp3 if fmt == "mp3" else q_mp4)
                else:
                    print(f"  ✗ error » file not found")
                continue
            
            smart_download(url, file_format=fmt, quality=q_mp3 if fmt == "mp3" else q_mp4)
            print("") 
        except KeyboardInterrupt:
            print("\nbye.")
            break
        except Exception as e:
            print(f"  !")

def main():
    parser = argparse.ArgumentParser(description="ytmpcli: A simple YouTube downloader for MP3 and MP4.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--n", metavar="URL", help="Download a single video (normal)")
    group.add_argument("--p", metavar="URL", help="Download an entire playlist")
    parser.add_argument("-f", "--format", choices=["mp3", "mp4"], default="mp3", help="Output format")

    if len(sys.argv) == 1:
        interactive_mode()
        return

    args = parser.parse_args()
    if args.n or args.p:
        url = args.n or args.p
        is_playlist = bool(args.p)
        print(f"Initiating download in {args.format.upper()} format...")
        download_media(url, is_playlist=is_playlist, file_format=args.format)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
