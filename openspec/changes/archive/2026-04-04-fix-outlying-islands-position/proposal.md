## Why

目前地圖投影使用 `geoMercator().fitSize()` 自動適配整個 GeoJSON 範圍。金門縣（經度 ~118°E）與連江縣（~120°E）位於台灣本島（120°-122°E）西北方遠處，導致 bounding box 橫向擴展約 51%，台灣本島在 SVG 中被壓縮、顯示過小，降低了地圖的可讀性與互動體驗。

## What Changes

- 修改 `createProjection()` 邏輯：投影僅依據台灣本島（含澎湖）的範圍計算 fitSize，確保本島佔滿地圖大部分空間
- 對金門縣、連江縣的地理座標施加偏移（offset），將其視覺位置搬移至台灣本島西南方附近，使其在地圖上可見且不影響本島比例
- 在地圖上為偏移後的離島加上虛線框標示，讓使用者理解這些區域經過位置調整

## 非目標

- 不移除金門縣或連江縣的地圖資料
- 不修改 TopoJSON 原始檔案（偏移在前端渲染時動態處理）
- 不調整澎湖縣的位置（澎湖距離本島較近，不影響整體比例）
- 不修改 API 端點或後端邏輯

## 技術可行性

- D3.js 支援對 GeoJSON features 進行座標偏移（透過在投影前修改座標或在 path 繪製後使用 SVG `transform`）
- 使用 SVG `transform: translate()` 對已繪製的離島路徑進行平移是最簡單的方式，不需修改原始地理資料
- 許多台灣政府官方地圖（如中選會、國發會）皆採用類似的離島位移處理方式

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `taiwan-map-page`：修改地圖投影計算邏輯，新增離島位置偏移與虛線框標示

## Impact

- **前端 JS**：`static/js/map.js` 修改 `createProjection()`、`drawCounties()`、`drillDown()` 函式
