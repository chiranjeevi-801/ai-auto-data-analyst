"""
tests/test_ingestion.py

Unit tests for data ingestion modules.
"""
import os
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.data_ingestion.file_uploader import handle_upload
from modules.data_ingestion.url_importer import download_from_url


# ─────────────────────────────────────────
# Stub for Streamlit's uploadedFile object
# ─────────────────────────────────────────
class FakeUploadedFile:
    def __init__(self, name, content: bytes):
        self.name = name
        self._content = content

    def getbuffer(self):
        return self._content


# ─── Tests ───────────────────────────────
def test_handle_upload_csv(tmp_path, monkeypatch):
    """handle_upload should write the file to the raw data directory."""
    import config.settings as settings
    monkeypatch.setattr(settings, "RAW_DATA_DIR", str(tmp_path))

    csv_bytes = b"name,age\nAlice,30\nBob,25\n"
    fake_file = FakeUploadedFile("test_upload.csv", csv_bytes)
    path = handle_upload(fake_file)

    assert path is not None, "handle_upload returned None"
    assert os.path.exists(path), "Uploaded file not found on disk"

    df = pd.read_csv(path)
    assert len(df) == 2
    assert list(df.columns) == ["name", "age"]


def test_handle_upload_none():
    """handle_upload should return None when no file is given."""
    result = handle_upload(None)
    assert result is None


def test_download_from_url_bad_url(tmp_path, monkeypatch):
    """download_from_url should return None on an invalid URL."""
    import config.settings as settings
    monkeypatch.setattr(settings, "RAW_DATA_DIR", str(tmp_path))

    result = download_from_url("http://localhost:9/nonexistent.csv", "out.csv")
    assert result is None
