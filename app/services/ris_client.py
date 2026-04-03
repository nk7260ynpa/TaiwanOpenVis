"""戶政司開放資料 API 客戶端。"""

import logging
from typing import Any

import requests

from app.utils.cache import read_cache, write_cache

logger = logging.getLogger(__name__)

BASE_URL = "https://www.ris.gov.tw/rs-opendata/api/v1/datastore"


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
    """擷取各縣市人口密度資料（ODRP048）。

    Args:
        year: 民國年份，預設 113。

    Returns:
        標準化後的縣市人口密度列表。
    """
    raw = _fetch_all_pages("ODRP048", year)
    return [
        {
            "county": item["site_id"],
            "population": int(item["people_total"]),
            "area": float(item["area"]),
            "density": int(item["population_density"]),
        }
        for item in raw
    ]


def fetch_town_population(year: str = "113") -> list[dict[str, Any]]:
    """擷取各鄉鎮市區戶數與人口資料（ODRP019）。

    Args:
        year: 民國年份，預設 113。

    Returns:
        標準化後的鄉鎮人口列表。
    """
    raw = _fetch_all_pages("ODRP019", year)
    result = []
    for item in raw:
        male = (
            int(item.get("共同生活戶_男", 0))
            + int(item.get("共同事業戶_男", 0))
            + int(item.get("單獨生活戶_男", 0))
        )
        female = (
            int(item.get("共同生活戶_女", 0))
            + int(item.get("共同事業戶_女", 0))
            + int(item.get("單獨生活戶_女", 0))
        )
        households = (
            int(item.get("共同生活戶_戶數", 0))
            + int(item.get("共同事業戶_戶數", 0))
            + int(item.get("單獨生活戶_戶數", 0))
        )
        result.append({
            "county": item.get("區域別", ""),
            "town": item.get("村里名稱", ""),
            "households": households,
            "male": male,
            "female": female,
            "population": male + female,
        })
    return result


def fetch_and_cache_all():
    """擷取所有人口資料並快取至本地。"""
    logger.info("開始擷取縣市人口密度資料...")
    counties = fetch_county_density()
    write_cache("counties.json", counties)

    logger.info("開始擷取鄉鎮人口資料...")
    towns = fetch_town_population()
    write_cache("towns.json", towns)

    logger.info("所有人口資料快取完成")
