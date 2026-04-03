"""戶政司開放資料 API 客戶端。"""

import logging
from collections import defaultdict
from typing import Any

import requests

from app.utils.cache import read_cache, write_cache

logger = logging.getLogger(__name__)

BASE_URL = "https://www.ris.gov.tw/rs-opendata/api/v1/datastore"


def _normalize_name(name: str) -> str:
    """將地名中的「臺」正規化為「台」，與 TopoJSON 一致。"""
    return name.replace("臺", "台")


def _extract_county(site_id: str) -> str:
    """從 site_id（如「新北市板橋區」）取出縣市名稱（前三個字）。"""
    return site_id[:3]


def _extract_town(site_id: str) -> str:
    """從 site_id（如「新北市板橋區」）取出鄉鎮名稱（第四個字起）。"""
    return site_id[3:]


def _fetch_all_pages(endpoint: str, param: str) -> list[dict[str, Any]]:
    """從戶政司 API 擷取指定端點的所有分頁資料。

    Args:
        endpoint: API 端點名稱，例如 "ODRP048"。
        param: 年份或年月參數，例如 "113"。

    Returns:
        所有分頁的 responseData 合併後的列表。
    """
    all_data: list[dict[str, Any]] = []
    page = 1

    while True:
        url = f"{BASE_URL}/{endpoint}/{param}"
        params = {"PAGE": str(page)}
        logger.info("擷取 %s 第 %d 頁...", url, page)

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()

        data = result.get("responseData", [])
        all_data.extend(data)

        total_page = int(result.get("totalPage", "1"))
        if page >= total_page:
            break
        page += 1

    logger.info("擷取 %s 完成，共 %d 筆", endpoint, len(all_data))
    return all_data


def fetch_county_density(year: str = "113") -> list[dict[str, Any]]:
    """擷取各縣市人口密度資料（ODRP048，鄉鎮層級聚合為縣市）。

    ODRP048 回傳 370 筆鄉鎮資料，此函式聚合為 22 個縣市。

    Args:
        year: 民國年份，預設 113。

    Returns:
        標準化後的縣市人口密度列表。
    """
    raw = _fetch_all_pages("ODRP048", year)

    county_agg: dict[str, dict[str, float]] = defaultdict(
        lambda: {"population": 0, "area": 0.0}
    )
    for item in raw:
        try:
            population = int(item["people_total"])
            area = float(item["area"])
        except (ValueError, TypeError):
            logger.debug("跳過無效資料: %s", item.get("site_id"))
            continue
        county = _normalize_name(_extract_county(item["site_id"]))
        county_agg[county]["population"] += population
        county_agg[county]["area"] += area

    return [
        {
            "county": county,
            "population": int(data["population"]),
            "area": round(data["area"], 4),
            "density": round(data["population"] / data["area"])
            if data["area"] > 0
            else 0,
        }
        for county, data in sorted(county_agg.items())
    ]


def fetch_town_population(year: str = "113") -> list[dict[str, Any]]:
    """擷取各鄉鎮市區戶數與人口資料（ODRP019，村里層級聚合為鄉鎮）。

    ODRP019 回傳約 7,700 筆村里資料，此函式聚合為鄉鎮層級。

    Args:
        year: 民國年份，預設 113。

    Returns:
        標準化後的鄉鎮人口列表。
    """
    raw = _fetch_all_pages("ODRP019", year)

    town_agg: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"households": 0, "male": 0, "female": 0}
    )
    def _safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0

    for item in raw:
        site = item.get("區域別", "")
        if len(site) < 3:
            continue
        county = _normalize_name(_extract_county(site))
        town = _extract_town(site)
        key = (county, town)

        male = (
            _safe_int(item.get("共同生活戶_男", 0))
            + _safe_int(item.get("共同事業戶_男", 0))
            + _safe_int(item.get("單獨生活戶_男", 0))
        )
        female = (
            _safe_int(item.get("共同生活戶_女", 0))
            + _safe_int(item.get("共同事業戶_女", 0))
            + _safe_int(item.get("單獨生活戶_女", 0))
        )
        households = (
            _safe_int(item.get("共同生活戶_戶數", 0))
            + _safe_int(item.get("共同事業戶_戶數", 0))
            + _safe_int(item.get("單獨生活戶_戶數", 0))
        )
        town_agg[key]["households"] += households
        town_agg[key]["male"] += male
        town_agg[key]["female"] += female

    return [
        {
            "county": county,
            "town": town,
            "households": data["households"],
            "male": data["male"],
            "female": data["female"],
            "population": data["male"] + data["female"],
        }
        for (county, town), data in sorted(town_agg.items())
    ]


def fetch_and_cache_all():
    """擷取所有人口資料並快取至本地。"""
    logger.info("開始擷取縣市人口密度資料...")
    counties = fetch_county_density()
    write_cache("counties.json", counties)

    logger.info("開始擷取鄉鎮人口資料...")
    towns = fetch_town_population()
    write_cache("towns.json", towns)

    logger.info("所有人口資料快取完成")
