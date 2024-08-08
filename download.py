from pathlib import Path

import yt_dlp


def download(url: str, path: Path = Path("/sdcard/Download")):
    outtmpl = str(path / "%(title)s.%(ext)s") if path.is_dir() else str(path)
    folder = path if path.is_dir() else path.parent
    folder.mkdir(parents=True, exist_ok=True)
    opts = {"outtmpl": outtmpl}
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
