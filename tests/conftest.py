"""測試共用 fixtures。"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.utils.cache import DATA_DIR


@pytest.fixture(autouse=True)
def setup_test_cache(tmp_path):
    """使用暫時目錄作為快取，避免影響正式資料。"""
    with patch("app.utils.cache.DATA_DIR", tmp_path):
        with patch("app.services.ris_client.read_cache") as mock_read:
            with patch("app.services.ris_client.write_cache"):
                mock_read.return_value = None
                yield tmp_path


@pytest.fixture()
def sample_counties():
    """縣市人口密度範例資料。"""
    return [
        {"county": "台北市", "population": 2492883, "area": 271.7997, "density": 9172},
        {"county": "新北市", "population": 4032966, "area": 2052.5667, "density": 1965},
        {"county": "桃園市", "population": 2294328, "area": 1220.9540, "density": 1879},
    ]


@pytest.fixture()
def sample_towns():
    """鄉鎮人口範例資料。"""
    return [
        {"county": "台北市", "town": "中正區", "households": 67000, "male": 76000, "female": 82000, "population": 158000},
        {"county": "台北市", "town": "大安區", "households": 130000, "male": 143000, "female": 161000, "population": 304000},
        {"county": "新北市", "town": "板橋區", "households": 237000, "male": 268000, "female": 286000, "population": 554000},
    ]


@pytest.fixture()
def client(sample_counties, sample_towns):
    """建立測試用 FastAPI TestClient。"""
    with patch("app.routers.population.read_cache") as mock_read:
        def side_effect(filename):
            if filename == "counties.json":
                return sample_counties
            if filename == "towns.json":
                return sample_towns
            return None

        mock_read.side_effect = side_effect

        with patch("app.services.ris_client.fetch_and_cache_all"):
            from app.main import app
            yield TestClient(app)
