"""TaiwanOpenVis FastAPI 應用程式入口。"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routers import population
from app.services.ris_client import fetch_and_cache_all

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期：啟動時擷取並快取人口資料。"""
    logger.info("應用程式啟動，開始擷取人口資料...")
    try:
        fetch_and_cache_all()
        logger.info("人口資料快取完成")
    except Exception:
        logger.warning("啟動時擷取人口資料失敗，將使用既有快取", exc_info=True)
    yield
    logger.info("應用程式關閉")


app = FastAPI(title="TaiwanOpenVis", lifespan=lifespan)

app.include_router(population.router, prefix="/api")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    """首頁。"""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/map", response_class=HTMLResponse)
async def map_page():
    """地圖頁。"""
    return FileResponse(STATIC_DIR / "map.html")


@app.get("/detail/{county}", response_class=HTMLResponse)
async def detail_page(county: str):
    """資料詳情頁。"""
    return FileResponse(STATIC_DIR / "detail.html")
