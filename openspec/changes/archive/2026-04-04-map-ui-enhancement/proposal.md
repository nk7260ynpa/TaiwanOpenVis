## Why

目前地圖頁面以人口密度作為縣市層級色彩指標，但使用者更直覺地關心「人口數」多寡；頁面標題佔據地圖上方空間，壓縮了地圖可視區域；且網站缺乏暗色模式，在低光環境下閱讀體驗不佳。本次變更統一改善地圖頁面的資訊呈現方式並提供暗色模式支援。

## What Changes

- 縣市層級 Choropleth 色彩指標從「人口密度」改為「人口數」，鄉鎮層級維持人口數不變
- 將「台灣人口分佈地圖 / 點擊縣市可查看鄉鎮市區的人口分佈」標題文字從頁面頂部移至地圖 SVG 內部左上角，以 overlay 方式呈現
- 新增暗色模式（dark mode），支援手動切換與系統偏好自動偵測

## 非目標

- 不變更 API 端點或後端邏輯
- 不新增資料來源或資料集
- 不重新設計整體頁面佈局結構

## 技術可行性

- 色彩指標變更僅需修改 `createColorScale()` 的 `valueKey` 參數與圖例文字，技術風險極低
- 標題移入 SVG 可透過 D3.js `text` 元素實現，不影響地圖投影與互動邏輯
- 暗色模式可透過 CSS 變數（CSS Custom Properties）切換色彩主題，搭配 `prefers-color-scheme` media query 與 JavaScript toggle 實現，不需引入額外依賴

## Capabilities

### New Capabilities

- `dark-mode`: 網站暗色模式支援，包含色彩主題切換機制與切換按鈕

### Modified Capabilities

- `taiwan-map-page`: 縣市層級色彩指標從人口密度改為人口數；頁面標題移入地圖 SVG 內部左上角
- `web-layout`: 新增暗色模式相關的 CSS 變數定義與主題切換 UI 元件

## Impact

- **前端 CSS**：`static/css/style.css` 新增暗色主題變數與切換樣式
- **前端 JS**：`static/js/map.js` 修改色彩指標與新增 SVG 內文字元素
- **前端 JS**：`static/js/common.js` 新增暗色模式切換邏輯
- **前端 HTML**：`static/map.html` 移除頁面標題區塊，導覽列新增切換按鈕
- **前端 HTML**：`static/index.html`、`static/detail.html` 導覽列新增切換按鈕
