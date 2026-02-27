import argparse
import sys
from .downloader import download_media, smart_download
import os

def interactive_mode():
    os.system('cls' if os.name == 'nt' else 'clear')
    home = os.path.expanduser("~")
    target = os.path.join(home, "Downloads", "ytmpcli")
    
    fmt = "audio"
    q_video = "1080"
    
    header = """
    █▄█ ▀█▀ █▀▄▀█ █▀█ █▀▀ █   █
    ░█░ ░█░ █░▀░█ █▀▀ █▄▄ █▄▄ █
    
    by NamikazeAsh
    """
    print(header)
    print(f"  ready  » {target}")
    print(f"  inputs » [link], [audio/video], [res], [?], or [q]uit")
    print("  " + "─" * 55)

    while True:
        try:
            curr_mode = "audio" if fmt == "audio" else f"video:{q_video}p"
            prompt = f"\n  link ({curr_mode}) > "
            url = input(prompt).strip()
            
            if not url: continue
            if url.lower() in ['exit', 'quit', 'q']: break
            
            if url == '?':
                print("\n  [ commands ]")
                print("  audio, video : switch mode")
                print("  res          : change video res")
                print("  s:<query>    : search & download top result")
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
                smart_download(search_url, file_format=fmt, quality='best' if fmt == "audio" else q_video)
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
            
            smart_download(url, file_format=fmt, quality='best' if fmt == "audio" else q_video)
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
