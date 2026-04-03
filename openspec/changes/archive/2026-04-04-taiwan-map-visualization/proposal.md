## Why

目前專案尚無任何前端頁面與視覺化實作。作為首個可交付功能，以台灣地圖呈現人口分佈資料是最直觀的切入點——使用者一眼就能看出各縣市、鄉鎮的人口差異。資料來源為內政部戶政司開放資料 API（ris.gov.tw），免認證、JSON 格式，技術可行性高。

## What Changes

- 建立 FastAPI 後端服務，代理戶政司 API 並快取人口資料
- 建立前端頁面，以 D3.js 繪製台灣縣市層級的 Choropleth 地圖
- 滑鼠懸停行政區時，在滑鼠游標旁顯示該區域的詳細資訊（tooltip 跟隨滑鼠移動）
- 提供鄉鎮市區層級的下鑽功能（點擊縣市可查看鄉鎮細節）
- 設計首頁、地圖頁、資料詳情頁三個頁面
- 提供 Docker 化的完整部署方案

## 非目標

- 不實作村里層級的地圖視覺化（初期僅到鄉鎮層級）
- 不建立使用者帳號或個人化功能
- 不實作資料匯出或下載功能
- 不處理即時資料串流，僅定期快取

## 技術可行性評估

- **資料來源**：戶政司 ODRP048 端點提供 370 筆鄉鎮人口密度資料（年度），ODRP019 提供村里戶數（年度），均為免認證 JSON API
- **地圖底圖**：政府開放資料平台提供台灣縣市與鄉鎮的 GeoJSON/TopoJSON 行政區邊界資料
- **前端渲染**：D3.js 原生支援 GeoJSON 投影與 Choropleth 繪製，效能足以處理 370 筆多邊形

## Capabilities

### New Capabilities

- `population-data-api`: 後端 API 服務，擷取並快取戶政司人口資料，提供給前端查詢
- `taiwan-map-page`: 台灣地圖視覺化頁面，以 Choropleth 呈現人口分佈並支援縣市→鄉鎮下鑽
- `web-layout`: 網站整體頁面佈局，包含首頁、導覽列、共用元件

### Modified Capabilities

（無既有規格需修改）

## Impact

- 新增 `app/` 目錄：FastAPI 應用程式碼
- 新增 `static/` 目錄：前端 HTML/CSS/JS 與地圖資料
- 新增 `data/` 目錄：快取的人口資料 JSON
- 修改 `docker/`：更新 Dockerfile 與 build.sh 以支援 FastAPI 服務
- 修改 `run.sh`：啟動 Docker container 執行 FastAPI
- 新增 Python 依賴：fastapi, uvicorn, requests, pandas
