import re
from enum import Enum


class Platform(Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    FACEBOOK = "facebook"


PATTERNS: list[tuple[re.Pattern, Platform]] = [
    (re.compile(r"(youtube\.com|youtu\.be)"), Platform.YOUTUBE),
    (re.compile(r"tiktok\.com"), Platform.TIKTOK),
    (re.compile(r"instagram\.com"), Platform.INSTAGRAM),
    (re.compile(r"(twitter\.com|x\.com)"), Platform.TWITTER),
    (re.compile(r"(facebook\.com|fb\.com)"), Platform.FACEBOOK),
]


def parse_url(text: str) -> Platform | None:
    """Detect supported social network platform from a URL string."""
    for pattern, platform in PATTERNS:
        if pattern.search(text):
            return platform
    return None
