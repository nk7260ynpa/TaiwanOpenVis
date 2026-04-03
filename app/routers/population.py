"""人口資料 API 路由。"""

from fastapi import APIRouter

from app.utils.cache import get_cache_timestamp

router = APIRouter()


@router.get("/health")
async def health():
    """健康檢查端點。"""
    return {
        "status": "ok",
        "data_cached_at": get_cache_timestamp(),
    }
