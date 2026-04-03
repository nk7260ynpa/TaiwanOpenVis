# REST API 資料查詢服務

## 狀態

draft

## 概述

提供 REST API 讓前端視覺化儀表板查詢已處理的公開資料，支援篩選、排序與分頁功能。

## 需求

### API 端點

- `GET /api/datasets` — 列出所有可用資料集
- `GET /api/datasets/{dataset_id}` — 取得特定資料集的完整資料
- `GET /api/datasets/{dataset_id}/summary` — 取得資料集摘要統計
- `GET /api/health` — 健康檢查端點

### 查詢功能

- 支援依欄位篩選（query parameters）
- 支援排序（sort by field, asc/desc）
- 支援分頁（offset/limit）

### 回應格式

- 統一使用 JSON 格式回應
- 包含 metadata（總筆數、分頁資訊）
- 錯誤回應遵循統一格式

## 非目標

- 不實作使用者認證與授權機制（初期為公開 API）
- 不提供資料寫入端點
- 不實作 GraphQL

## 技術方案

- 使用 FastAPI 框架
- 透過 Docker container 部署
- API 文件自動產生（Swagger UI）
