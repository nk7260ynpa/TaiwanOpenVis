## Context

TaiwanOpenVis 地圖使用 `d3.geoMercator().fitSize([800, 1000], geojson)` 自動計算投影參數。當 GeoJSON 包含金門（~118°E）和連江（~120°E）時，bounding box 經度寬度從本島的 2.56° 擴展到 3.86°（+51%），導致本島顯示比例被壓縮約 8.5%。

目前 `map.js` 的 `createProjection()` 對所有 features 一視同仁，沒有離島的特殊處理。

## Goals / Non-Goals

**Goals:**
- 投影計算僅基於本島範圍，讓台灣本島佔滿地圖大部分空間
- 金門、連江仍可見，但位置經過偏移，顯示於地圖左下角附近
- 離島區域以虛線框標示，避免使用者誤解地理位置

**Non-Goals:**
- 不修改 TopoJSON 原始資料
- 不調整澎湖縣位置
- 不為離島建立獨立的 inset map

## Decisions

### 決策 1：投影計算排除離島

**選擇**：在 `createProjection()` 中，先過濾出「非金門、非連江」的 features 建立 fitSize 用的 GeoJSON，再以完整 GeoJSON 建立 path。

**理由**：這是最小變更方案。投影以本島為基準，所有 features 都用同一個 projection 繪製，只是離島會落在 SVG 邊緣或外部。

**替代方案**：
- 固定投影 scale/translate 常數 → 不同資料來源的 TopoJSON 需重新計算，維護性差
- 修改 TopoJSON 檔案中的座標 → 破壞原始地理資料，不可逆

### 決策 2：SVG transform 偏移離島路徑

**選擇**：繪製完所有 path 後，對 COUNTYNAME 為「金門縣」或「連江縣」的路徑元素施加 SVG `transform: translate(dx, dy)`，將其平移至台灣本島西南方（地圖左下角區域）。

**理由**：
- 在 D3.js path 繪製後操作，與投影計算完全解耦
- 不修改原始地理座標，偏移量容易調整
- 各官方地圖（中選會、氣象署）皆採用類似做法

**偏移量計算**：需根據實際投影結果觀察金門/連江原始渲染位置與目標位置的 pixel 差異。預計金門向右下偏移、連江向下偏移，使兩者集中在台灣本島左下方。

### 決策 3：虛線框標示偏移區域

**選擇**：在偏移後的離島周圍繪製虛線矩形（`stroke-dasharray`），並標註縣市名稱。

**理由**：視覺上明確告知使用者該區域為位置經調整的離島，是台灣地圖視覺化的常見慣例。

## Risks / Trade-offs

- **[風險] 偏移量需要根據實際渲染效果調校** → 先設定初始值，在瀏覽器中目視調整
- **[風險] 點擊離島觸發 drillDown 時，鄉鎮視圖投影正常（無需偏移）** → drillDown 使用 `createProjection(countyTowns)`，單一縣市的 fitSize 不受影響
- **[取捨] 離島位置不再反映真實地理方位** → 以虛線框標示作為視覺提示
