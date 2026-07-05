import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yt_dlp

from services.file_manager import get_temp_path


@dataclass
class FormatOption:
    """Represents a downloadable quality option presented to the user."""
    label: str
    format_id: str


@dataclass
class DownloadProgress:
    """Progress report sent back during a download via callback."""
    percent: float = 0.0
    speed: str = ""
    eta: str = ""


async def list_formats(url: str) -> list[FormatOption]:
    """Fetch available format options for a given URL using yt-dlp (runs in executor)."""

    def _sync_list() -> list[FormatOption]:
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            if not formats:
                return [_best_option(info)]
            return _group_formats(formats, info)

    return await asyncio.to_thread(_sync_list)


def _best_option(info: dict) -> FormatOption:
    return FormatOption(label="🎬 Mejor calidad", format_id="bestvideo+bestaudio/best")


def _group_formats(formats: list[dict], info: dict) -> list[FormatOption]:
    """Group available formats into 2-3 curated quality options."""
    options: list[FormatOption] = []

    # 1. Best quality (video + audio merged)
    options.append(FormatOption("🎬 Mejor calidad", "bestvideo+bestaudio/best"))

    # 2. Medium quality — try 720p, fall back to 480p
    medium = _find_medium_format(formats)
    if medium:
        label = f"📱 Mediana ({medium.get('height', '?')}p)"
        options.append(FormatOption(label, medium["format_id"]))

    # 3. Audio only
    options.append(FormatOption("🎵 Solo audio", "bestaudio/best"))

    return options


def _find_medium_format(formats: list[dict]) -> dict | None:
    """Find a ~720p or ~480p video-only format to offer as medium quality."""
    for height in (720, 480, 360):
        for f in formats:
            if f.get("height") == height and f.get("vcodec") != "none":
                return f
    return None


async def download(
    url: str,
    format_id: str,
    progress_callback: Callable[[DownloadProgress], None] | None = None,
) -> Path:
    """Download a video using yt-dlp (runs in executor). Returns path to downloaded file."""

    output_path = get_temp_path(".mp4")

    def _progress_hook(d: dict):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
            downloaded = d.get("downloaded_bytes", 0)
            percent = (downloaded / total) * 100
            p = DownloadProgress(
                percent=percent,
                speed=d.get("_speed_str", ""),
                eta=d.get("_eta_str", ""),
            )
            if progress_callback:
                progress_callback(p)

    def _sync_download():
        opts = {
            "format": format_id,
            "outtmpl": str(output_path),
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [_progress_hook],
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        return output_path

    return await asyncio.to_thread(_sync_download)
