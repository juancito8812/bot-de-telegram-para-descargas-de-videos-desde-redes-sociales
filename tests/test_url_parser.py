import pytest
from services.url_parser import Platform, parse_url


def test_parse_youtube():
    assert parse_url("https://www.youtube.com/watch?v=abc123") == Platform.YOUTUBE
    assert parse_url("https://youtu.be/abc123") == Platform.YOUTUBE


def test_parse_tiktok():
    assert parse_url("https://www.tiktok.com/@user/video/123456") == Platform.TIKTOK


def test_parse_instagram():
    assert parse_url("https://www.instagram.com/reel/ABC123/") == Platform.INSTAGRAM


def test_parse_twitter():
    assert parse_url("https://twitter.com/user/status/123456") == Platform.TWITTER
    assert parse_url("https://x.com/user/status/123456") == Platform.TWITTER


def test_parse_facebook():
    assert parse_url("https://www.facebook.com/watch/?v=123456") == Platform.FACEBOOK


def test_parse_unknown():
    assert parse_url("https://example.com/video") is None


def test_parse_no_url():
    assert parse_url("hello world") is None
