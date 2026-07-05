import pytest
from pathlib import Path
from services.file_manager import get_temp_path, cleanup_file, ensure_download_dir, is_within_limit


@pytest.mark.asyncio
async def test_ensure_download_dir_creates(tmp_path):
    d = tmp_path / "downloads"
    await ensure_download_dir(d)
    assert d.exists()


def test_get_temp_path_returns_unique():
    p1 = get_temp_path(".mp4")
    p2 = get_temp_path(".mp4")
    assert p1 != p2
    assert str(p1).endswith(".mp4")
    # Cleanup both
    Path(p1).unlink(missing_ok=True)
    Path(p2).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_cleanup_file_removes(tmp_path):
    f = tmp_path / "test.mp4"
    f.write_text("data")
    assert f.exists()
    await cleanup_file(f)
    assert not f.exists()


@pytest.mark.asyncio
async def test_cleanup_file_missing_does_not_raise(tmp_path):
    f = tmp_path / "missing.mp4"
    await cleanup_file(f)  # should not raise


def test_is_within_limit_under():
    assert is_within_limit(1024) is True


def test_is_within_limit_over():
    assert is_within_limit(100 * 1024 * 1024) is False


def test_is_within_limit_exact():
    assert is_within_limit(50 * 1024 * 1024) is True
