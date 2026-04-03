# TaiwanOpenVis

台灣公開資料視覺化專案，將台灣政府公開資料透過互動式地圖與圖表呈現，讓使用者能直觀地探索與理解資料。

## 功能

- 台灣縣市人口密度 Choropleth 地圖
- 點擊縣市下鑽至鄉鎮市區層級
- 滑鼠懸停顯示人口詳細資訊
- 鄉鎮人口資料表格（支援排序）
- 響應式設計（桌面與行動裝置）

## 技術棧

- **後端**：Python（FastAPI, Pandas）
- **前端**：HTML/CSS/JavaScript（D3.js）
- **資料來源**：內政部戶政司開放資料 API
- **部署**：Docker

## 專案架構

```
TaiwanOpenVis/
├── app/              # FastAPI 後端應用
│   ├── main.py       # 應用入口
│   ├── routers/      # API 路由
│   ├── services/     # 外部 API 客戶端
│   └── utils/        # 工具模組
├── static/           # 前端靜態檔案
│   ├── index.html    # 首頁
│   ├── map.html      # 地圖頁
│   ├── detail.html   # 詳情頁
│   ├── css/          # 樣式表
│   ├── js/           # JavaScript
│   └── data/         # TopoJSON 地圖底圖
├── tests/            # 單元測試
├── docker/           # Docker 相關設定
│   ├── build.sh      # 建立 Docker image
│   └── Dockerfile    # Docker image 定義
├── openspec/         # OpenSpec 專案規格
├── data/             # API 資料快取（自動產生）
├── logs/             # 日誌檔案
├── requirements.txt  # Python 依賴
├── run.sh            # 啟動腳本
└── LICENSE           # Apache 2.0
```

## 快速開始

### 啟動服務

```bash
bash run.sh
```

此腳本會自動建置 Docker image 並啟動 container，服務預設於 `http://localhost:8000`。

### 執行測試

```bash
docker run --rm -v "$(pwd)/tests:/app/tests" taiwan-open-vis python -m pytest tests/ -v
```

## API 端點

| 端點 | 說明 |
|------|------|
| `GET /` | 首頁 |
| `GET /map` | 人口地圖頁 |
| `GET /detail/{county}` | 縣市資料詳情頁 |
| `GET /api/population/counties` | 縣市人口密度 JSON |
| `GET /api/population/towns/all` | 全部鄉鎮人口 JSON |
| `GET /api/population/towns/{county}` | 指定縣市的鄉鎮人口 JSON |
| `GET /api/health` | 健康檢查 |

## 授權條款

本專案採用 [Apache License 2.0](LICENSE) 授權。
