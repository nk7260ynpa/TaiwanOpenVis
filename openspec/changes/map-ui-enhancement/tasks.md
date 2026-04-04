## 1. 地圖色彩指標調整

- [x] 1.1 修改 `static/js/map.js` 的 `drawCounties()` 函式，將 `createColorScale(countyData, "density")` 改為 `createColorScale(countyData, "population")`，並更新圖例文字為「人口數」。驗收：縣市層級地圖色彩依人口數深淺呈現，圖例標示「人口數」

## 2. 地圖內嵌標題

- [x] 2.1 移除 `static/map.html` 中的 `.page-header` 區塊（標題與副標題 HTML 元素）。驗收：地圖頁面不再顯示獨立的頁面標題區塊
- [x] 2.2 在 `static/js/map.js` 的 `drawCounties()` 函式中，新增 SVG `<text>` 元素於左上角，顯示主標題「台灣人口分佈地圖」與副標題「點擊縣市可查看鄉鎮市區的人口分佈」，搭配半透明背景矩形。驗收：地圖 SVG 左上角顯示標題文字且可讀
- [x] 2.3 在 `static/js/map.js` 的 `drillDown()` 函式中，更新 SVG 內嵌標題為該縣市名稱。驗收：進入鄉鎮視圖時標題顯示縣市名稱

## 3. 暗色模式 CSS 變數

- [x] 3.1 在 `static/css/style.css` 新增 `[data-theme="dark"]` 選擇器，定義暗色主題的 CSS 變數（`--bg`, `--bg-card`, `--text`, `--text-light`, `--border`, `--primary` 等）。驗收：當 `<html>` 設定 `data-theme="dark"` 時，頁面配色切換為暗色
- [x] 3.2 在 `static/css/style.css` 新增 `@media (prefers-color-scheme: dark)` 規則，作為未儲存偏好時的預設值。驗收：系統偏好為暗色時網站自動套用暗色主題
- [x] 3.3 調整暗色模式下的地圖相關樣式：卡片背景、地圖邊框色、tooltip 背景。驗收：暗色模式下地圖 Choropleth 色彩對比清晰

## 4. 主題切換功能

- [ ] 4.1 在 `static/js/common.js` 新增主題切換邏輯：讀取 `localStorage` 偏好 → 若無則偵測 `prefers-color-scheme` → 套用 `data-theme` 屬性至 `<html>`。驗收：頁面載入時正確套用已儲存偏好或系統偏好
- [ ] 4.2 在 `static/js/common.js` 新增 `toggleTheme()` 函式，切換 `data-theme` 並存入 `localStorage`。驗收：呼叫函式後主題切換且偏好持久化
- [ ] 4.3 在所有頁面的導覽列（`index.html`, `map.html`, `detail.html`）新增主題切換按鈕，綁定 `toggleTheme()`。驗收：所有頁面導覽列顯示切換按鈕，點擊後主題切換

## 5. 暗色模式下地圖適配

- [ ] 5.1 修改 `static/js/map.js` 中的地圖邊框色（`stroke`），根據目前主題動態調整：亮色模式 `#fff`、暗色模式 `#555`。驗收：暗色模式下地圖區塊邊框清晰可見
- [ ] 5.2 修改 SVG 內嵌標題文字色彩，根據目前主題動態調整。驗收：暗色模式下標題文字清晰可讀

## 6. 測試與驗證

- [ ] 6.1 重啟 Docker container 並在瀏覽器中驗證：縣市地圖色彩改為人口數指標、標題位於地圖內左上角、暗色模式切換正常。驗收：三項功能均正常運作
