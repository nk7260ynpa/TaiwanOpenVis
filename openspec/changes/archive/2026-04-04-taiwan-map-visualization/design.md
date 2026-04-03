## Context

專案目前僅有 openspec 規格文件，尚無任何程式碼。此為首個功能實作，需從零建立完整的前後端架構。資料來源為內政部戶政司開放資料 API（免認證 JSON），地圖底圖需取得台灣行政區邊界的 GeoJSON。

## Goals / Non-Goals

**Goals:**

- 建立可重複使用的 FastAPI 後端框架，作為未來擴充的基礎
- 以 D3.js Choropleth 地圖呈現縣市與鄉鎮層級的人口分佈
- 提供完整的 Docker 化部署方案
- 頁面支援響應式設計（RWD）

**Non-Goals:**

- 不建立資料庫（以 JSON 檔案快取為主）
- 不實作村里層級地圖
- 不實作使用者認證或個人化功能

## Decisions

### D1: 前端架構 — 純靜態 HTML/JS，不使用框架

**選擇**：HTML + CSS + D3.js，由 FastAPI 提供靜態檔案服務

**替代方案**：
- React/Vue SPA：增加建置複雜度，對三個頁面的規模來說過重
- Jinja2 模板：伺服器端渲染，但地圖互動邏輯仍需大量 JS，混用反而更複雜

**理由**：專案規模小（3 個頁面），D3.js 本身就需要直接操作 DOM。純靜態檔案方便開發除錯，未來如需遷移至框架也容易。

### D2: 地圖底圖 — 使用 TopoJSON 格式

**選擇**：預先下載台灣行政區 TopoJSON 放入 `static/data/` 目錄

**替代方案**：
- GeoJSON：檔案體積較大（約 5-10 倍），載入速度慢
- 即時從外部 API 載入：增加外部依賴，頁面載入不穩定

**理由**：TopoJSON 經拓撲壓縮後檔案小（縣市約 100KB，鄉鎮約 500KB），D3.js 原生支援。預先下載避免執行期外部依賴。

### D3: 資料快取策略 — 啟動時擷取 + 檔案快取

**選擇**：應用程式啟動時從戶政司 API 擷取最新資料，存入 `data/` 目錄的 JSON 檔案。後續請求讀取本地檔案。

**替代方案**：
- 每次請求即時呼叫外部 API：延遲高且有流量限制風險
- 定時排程（cron）：啟動時快取已足夠，人口資料為月度/年度更新

**理由**：人口資料更新頻率低（月度/年度），啟動時擷取一次即可。重啟 container 即可更新資料。

### D4: 目錄結構

```
TaiwanOpenVis/
├── app/                    # FastAPI 應用
│   ├── main.py             # 應用入口，掛載路由與靜態檔案
│   ├── routers/
│   │   └── population.py   # 人口資料 API 路由
│   ├── services/
│   │   └── ris_client.py   # 戶政司 API 客戶端
│   └── utils/
│       └── cache.py        # 檔案快取工具
├── static/                 # 前端靜態檔案
│   ├── index.html          # 首頁
│   ├── map.html            # 地圖頁
│   ├── detail.html         # 資料詳情頁
│   ├── css/
│   │   └── style.css       # 樣式表
│   ├── js/
│   │   ├── map.js          # D3.js 地圖邏輯
│   │   ├── detail.js       # 詳情頁邏輯
│   │   └── common.js       # 共用工具函式
│   └── data/
│       ├── taiwan-counties.topojson   # 縣市邊界
│       └── taiwan-towns.topojson      # 鄉鎮邊界
├── data/                   # 快取的 API 資料
├── tests/                  # 單元測試
├── docker/
├── requirements.txt
└── run.sh
```

### D5: API 端點設計

| 端點 | 方法 | 說明 |
|------|------|------|
| `/` | GET | 首頁（靜態 HTML） |
| `/map` | GET | 地圖頁（靜態 HTML） |
| `/detail/{county}` | GET | 詳情頁（靜態 HTML） |
| `/api/population/counties` | GET | 各縣市人口密度資料 |
| `/api/population/towns/{county}` | GET | 特定縣市的鄉鎮人口資料 |
| `/api/health` | GET | 健康檢查 |

## Risks / Trade-offs

| 風險 | 緩解措施 |
|------|---------|
| 戶政司 API 無法連線（維護/異常） | 啟動時快取 + 保留上一次的快取檔案作為 fallback |
| TopoJSON 行政區邊界與戶政司資料的地名不一致 | 建立地名對照表（mapping），在資料處理層統一 |
| 鄉鎮層級 TopoJSON 檔案較大，行動裝置載入慢 | 使用簡化後的幾何資料，控制在 500KB 以內 |
| D3.js 在舊版瀏覽器相容性問題 | 鎖定 D3.js v7+，支援現代瀏覽器即可 |
