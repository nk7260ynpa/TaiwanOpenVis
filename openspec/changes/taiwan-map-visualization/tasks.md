## 1. 專案基礎建設

- [x] 1.1 建立 `requirements.txt`（fastapi, uvicorn, requests, pandas）並更新 `docker/Dockerfile` 安裝依賴。驗收：`docker build` 成功
- [x] 1.2 建立 `app/main.py` FastAPI 應用入口，掛載靜態檔案目錄（`static/`）與 API 路由。驗收：`uvicorn app.main:app` 可啟動且 `/api/health` 回傳 200
- [x] 1.3 更新 `docker/build.sh` 與 `run.sh`，支援建置並啟動 FastAPI container。驗收：`bash run.sh` 可啟動服務並從瀏覽器存取

## 2. 資料擷取與快取

- [x] 2.1 建立 `app/services/ris_client.py`，實作戶政司 ODRP048（縣市人口密度）與 ODRP019（鄉鎮戶數人口）的 API 呼叫。驗收：呼叫函式可取回正確 JSON 資料
- [x] 2.2 建立 `app/utils/cache.py`，實作 JSON 檔案快取機制（讀取/寫入 `data/` 目錄）。驗收：寫入後可讀回相同資料，檔案不存在時回傳 None
- [x] 2.3 在 `app/main.py` 啟動事件中整合資料擷取邏輯，啟動時自動快取。驗收：啟動應用後 `data/` 目錄產生快取 JSON 檔案；外部 API 不可用時使用既有快取並記錄警告日誌

## 3. 人口資料 API

- [x] 3.1 建立 `app/routers/population.py`，實作 `GET /api/population/counties` 端點，回傳縣市人口密度資料。驗收：回傳 JSON 陣列含 22 筆縣市，每筆含 county/population/area/density 欄位
- [x] 3.2 實作 `GET /api/population/towns/{county}` 端點，回傳指定縣市的鄉鎮人口資料。驗收：請求 `臺北市` 回傳該市所有鄉鎮區資料；請求不存在縣市回傳 404
- [x] 3.3 實作 `GET /api/health` 端點，回傳服務狀態與快取時間。驗收：回傳 JSON 含 status 與 data_cached_at 欄位

## 4. 地圖底圖準備

- [x] 4.1 取得台灣縣市行政區邊界 TopoJSON，存入 `static/data/taiwan-counties.topojson`。驗收：檔案可被 D3.js 正確載入並繪製出台灣輪廓
- [x] 4.2 取得台灣鄉鎮市區行政區邊界 TopoJSON，存入 `static/data/taiwan-towns.topojson`。驗收：檔案包含所有鄉鎮市區的幾何資料
- [x] 4.3 驗證 TopoJSON 中的地名與戶政司 API 回傳的地名一致，若有差異則建立對照表。驗收：地圖上的每個區塊都能對應到人口資料

## 5. 前端共用元件

- [x] 5.1 建立 `static/css/style.css`，定義全站樣式（字體、配色、導覽列、響應式斷點）。驗收：導覽列在桌面顯示連結、768px 以下收合為漢堡選單
- [x] 5.2 建立 `static/js/common.js`，實作共用工具函式（API 呼叫封裝、數字格式化）。驗收：可從其他 JS 檔案引用

## 6. 首頁

- [x] 6.1 建立 `static/index.html`，包含導覽列、專案標題、簡介文字、前往地圖頁的按鈕。驗收：開啟 `/` 顯示完整首頁，點擊按鈕可導向 `/map`

## 7. 地圖頁面

- [x] 7.1 建立 `static/map.html` 頁面結構與 `static/js/map.js` 基本框架。驗收：頁面載入時呼叫 API 並取得資料
- [x] 7.2 實作縣市 Choropleth 地圖繪製，依人口密度填色並顯示圖例。驗收：地圖正確顯示 22 個縣市的色彩差異與圖例
- [x] 7.3 實作縣市懸停 tooltip（顯示縣市名稱、總人口、面積、密度）。驗收：滑鼠懸停顯示 tooltip，移開消失
- [x] 7.4 實作點擊縣市下鑽至鄉鎮視圖（動畫縮放 + 鄉鎮 Choropleth）。驗收：點擊縣市後地圖縮放並顯示鄉鎮層級色彩圖
- [x] 7.5 實作鄉鎮懸停 tooltip（鄉鎮名稱、戶數、男女人口、總人口）與「返回全台」按鈕。驗收：tooltip 正確顯示，點擊返回可回到縣市視圖
- [x] 7.6 實作地圖響應式縮放（SVG 自適應容器寬度）。驗收：調整視窗大小時地圖自動縮放且比例正確

## 8. 資料詳情頁

- [x] 8.1 建立 `static/detail.html` 與 `static/js/detail.js`，顯示縣市名稱與鄉鎮人口表格。驗收：開啟 `/detail/臺北市` 顯示該市所有鄉鎮的人口資料表格
- [x] 8.2 實作表格欄位點擊排序功能。驗收：點擊「總人口」欄位標題可切換升冪/降冪排序

## 9. Docker 化與測試

- [x] 9.1 確認 `docker/Dockerfile` 包含所有依賴與正確的啟動指令。驗收：`bash docker/build.sh && bash run.sh` 可完整啟動服務
- [x] 9.2 建立 `tests/` 目錄，撰寫 API 端點的單元測試。驗收：`pytest tests/` 全部通過
