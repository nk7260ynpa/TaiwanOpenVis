## ADDED Requirements

### Requirement: 縣市人口密度 API

系統 SHALL 提供 `GET /api/population/counties` 端點，回傳全台各縣市的人口密度資料。回應格式為 JSON，包含縣市名稱、總人口數、面積（平方公里）、人口密度（人/平方公里）。

#### Scenario: 成功取得縣市人口密度

- **WHEN** 客戶端發送 GET 請求至 `/api/population/counties`
- **THEN** 系統回傳 HTTP 200，JSON 陣列包含 22 個縣市，每筆含 `county`、`population`、`area`、`density` 欄位

#### Scenario: 快取資料不存在時自動擷取

- **WHEN** 本地快取檔案不存在，客戶端請求 `/api/population/counties`
- **THEN** 系統從戶政司 ODRP048 API 擷取資料、快取至本地檔案後回傳

### Requirement: 鄉鎮人口資料 API

系統 SHALL 提供 `GET /api/population/towns/{county}` 端點，回傳指定縣市底下各鄉鎮市區的人口資料。回應格式為 JSON，包含鄉鎮名稱、戶數、男性人口、女性人口、總人口。

#### Scenario: 成功取得特定縣市的鄉鎮資料

- **WHEN** 客戶端發送 GET 請求至 `/api/population/towns/臺北市`
- **THEN** 系統回傳 HTTP 200，JSON 陣列包含該縣市所有鄉鎮市區的人口統計

#### Scenario: 縣市名稱不存在

- **WHEN** 客戶端請求的縣市名稱不在資料中（如 `/api/population/towns/不存在市`）
- **THEN** 系統回傳 HTTP 404 與錯誤訊息

### Requirement: 啟動時資料擷取

系統 SHALL 在應用程式啟動時自動從戶政司開放資料 API 擷取最新的人口資料，並快取為本地 JSON 檔案。若擷取失敗，系統 SHALL 使用既有的快取檔案繼續運作。

#### Scenario: 啟動時成功擷取資料

- **WHEN** 應用程式啟動且戶政司 API 可連線
- **THEN** 系統擷取最新資料並更新 `data/` 目錄下的快取檔案

#### Scenario: 啟動時外部 API 不可用

- **WHEN** 應用程式啟動但戶政司 API 無法連線
- **THEN** 系統記錄警告日誌，並使用 `data/` 目錄下既有的快取檔案提供服務

### Requirement: 健康檢查端點

系統 SHALL 提供 `GET /api/health` 端點，回傳服務狀態與資料快取時間。

#### Scenario: 健康檢查回應

- **WHEN** 客戶端發送 GET 請求至 `/api/health`
- **THEN** 系統回傳 HTTP 200，JSON 包含 `status`（"ok"）與 `data_cached_at`（快取時間戳）
