import requests
import static_ffmpeg
import subprocess

static_ffmpeg.add_paths()

def get_mp3_duration(url):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", url
    ], timeout=30)

    time = int(out)
    return time

def get_mp3_size(url):
    response = requests.head(url)
    return int(response.headers.get('Content-Length', 0))