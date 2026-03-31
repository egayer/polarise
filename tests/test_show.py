"""Tests for cross-platform .show() file creation behavior."""
import platform
import tempfile
from pathlib import Path
from unittest.mock import patch

import polars as pl
import polarise  # noqa: F401  — registers .style() on pl.DataFrame


def _make_df():
    return pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})


def test_show_linux_writes_to_home(tmp_path, monkeypatch):
    """On Linux, show() must write the temp file to Path.home(), not /tmp/."""
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))

    opened_urls = []
    with patch("webbrowser.open_new_tab", side_effect=lambda url: opened_urls.append(url)):
        _make_df().style().show()

    assert len(opened_urls) == 1
    url = opened_urls[0]
    assert tmp_path.as_posix() in url
    files = list(tmp_path.glob("polarise_preview_*.html"))
    assert len(files) == 1
    file_path = files[0]
    assert "<html" in file_path.read_text(encoding="utf-8").lower()
    file_path.unlink()


def test_show_macos_writes_to_tmpdir(tmp_path, monkeypatch):
    """On macOS, show() writes the temp file to tempfile.gettempdir()."""
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(tempfile, "gettempdir", lambda: str(tmp_path))

    opened_urls = []
    with patch("webbrowser.open_new_tab", side_effect=lambda url: opened_urls.append(url)):
        _make_df().style().show()

    assert len(opened_urls) == 1
    url = opened_urls[0]
    assert tmp_path.as_posix() in url
    files = list(tmp_path.glob("polarise_preview_*.html"))
    assert len(files) == 1
    assert "<html" in files[0].read_text(encoding="utf-8").lower()
    files[0].unlink()


def test_show_windows_writes_to_tmpdir(tmp_path, monkeypatch):
    """On Windows, show() writes the temp file to tempfile.gettempdir()."""
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(tempfile, "gettempdir", lambda: str(tmp_path))

    opened_urls = []
    with patch("webbrowser.open_new_tab", side_effect=lambda url: opened_urls.append(url)):
        _make_df().style().show()

    assert len(opened_urls) == 1
    url = opened_urls[0]
    assert tmp_path.as_posix() in url
    files = list(tmp_path.glob("polarise_preview_*.html"))
    assert len(files) == 1
    assert "<html" in files[0].read_text(encoding="utf-8").lower()
    files[0].unlink()
