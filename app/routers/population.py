"""人口資料 API 路由。"""

import logging

from fastapi import APIRouter, HTTPException

from app.services.ris_client import fetch_county_density, fetch_town_population
from app.utils.cache import get_cache_timestamp, read_cache, write_cache

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/population/counties")
async def get_counties():
    """取得各縣市人口密度資料。"""
    data = read_cache("counties.json")
    if data is None:
        logger.info("縣市快取不存在，即時擷取...")
        data = fetch_county_density()
        write_cache("counties.json", data)
    return data


@router.get("/population/towns/all")
async def get_all_towns():
    """取得全部鄉鎮人口資料。"""
    data = read_cache("towns.json")
    if data is None:
        logger.info("鄉鎮快取不存在，即時擷取...")
        data = fetch_town_population()
        write_cache("towns.json", data)
    return data


@router.get("/population/towns/{county}")
async def get_towns(county: str):
    """取得指定縣市的鄉鎮人口資料。"""
    data = read_cache("towns.json")
    if data is None:
        logger.info("鄉鎮快取不存在，即時擷取...")
        data = fetch_town_population()
        write_cache("towns.json", data)

    towns = [item for item in data if item["county"] == county]
    if not towns:
        raise HTTPException(status_code=404, detail=f"找不到縣市：{county}")
    return towns


@router.get("/health")
async def health():
    """健康檢查端點。"""
    return {
        "status": "ok",
        "data_cached_at": get_cache_timestamp(),
    }
