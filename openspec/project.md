# TaiwanOpenVis

## 概述

將台灣政府公開資料透過視覺化方式呈現，讓使用者能以互動式圖表探索與理解資料。

## 目標

- 自動擷取台灣政府公開資料平台（data.gov.tw）的資料集
- 將原始資料清洗、轉換為適合視覺化的格式
- 提供互動式視覺化儀表板供使用者瀏覽
- 透過 REST API 提供資料查詢服務

## 技術架構

- **後端**：Python（FastAPI）
- **前端**：HTML/CSS/JavaScript（D3.js / Chart.js）
- **資料處理**：Pandas
- **部署**：Docker
- **日誌**：Python logging

## 系統架構圖

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  公開資料平台  │───▶│  資料處理管線  │───▶│   資料儲存    │
│ (data.gov.tw) │    │  (ETL)       │    │  (JSON/CSV)  │
└──────────────┘    └──────────────┘    └──────┬───────┘
                                               │
                                        ┌──────▼───────┐
                                        │   API 服務    │
                                        │  (FastAPI)    │
                                        └──────┬───────┘
                                               │
                                        ┌──────▼───────┐
                                        │  視覺化前端   │
                                        │ (D3.js)      │
                                        └──────────────┘
```

## 規格清單

| 規格 | 說明 | 狀態 |
|------|------|------|
| [data-pipeline](specs/data-pipeline.md) | 資料擷取與處理管線 | draft |
| [api-service](specs/api-service.md) | REST API 資料查詢服務 | draft |
| [visualization-dashboard](specs/visualization-dashboard.md) | 互動式視覺化儀表板 | draft |
