import httpx
import static_ffmpeg
import subprocess

static_ffmpeg.add_paths()

def get_mp3_duration(url):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", url
    ], timeout=30)

    duration = float(out.decode().strip())
    return int(duration)

def get_mp3_size(url):
    try:
        response = httpx.head(url, timeout=10, follow_redirects=True, verify=False)
        return int(response.headers.get('Content-Length', 0))
    except Exception:
        return 0