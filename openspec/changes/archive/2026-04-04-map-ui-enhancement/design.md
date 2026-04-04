## Context

TaiwanOpenVis 地圖頁面目前以人口密度作為縣市層級 Choropleth 色彩指標，頁面標題位於地圖上方獨立區塊，且網站僅提供亮色模式。本設計涵蓋三項 UI 改善：色彩指標調整、標題內嵌地圖、暗色模式支援。

現有架構：
- CSS 使用 `:root` CSS 變數定義色彩主題（`--primary`, `--bg`, `--text` 等）
- D3.js 透過 `createColorScale(data, valueKey)` 建立色彩比例尺
- 頁面標題以 `.page-header` HTML 元素呈現於地圖容器外部
- 所有頁面共用 `static/css/style.css` 樣式表

## Goals / Non-Goals

**Goals:**
- 縣市層級色彩指標改為人口數，提供更直覺的視覺呈現
- 標題文字內嵌於地圖 SVG，減少頁面空間佔用
- 提供暗色模式，支援手動切換與系統偏好自動偵測

**Non-Goals:**
- 不修改 API 端點或後端邏輯
- 不重構 D3.js 地圖渲染架構
- 不支援多種色彩主題（僅亮/暗兩種）

## Decisions

### 決策 1：色彩指標改用人口數

**選擇**：修改 `drawCounties()` 中 `createColorScale` 的 `valueKey` 從 `"density"` 改為 `"population"`。

**理由**：變更範圍極小（一行參數 + 圖例文字），且 `countyData` 已包含 `population` 欄位，無需額外資料處理。

**替代方案**：提供下拉選單讓使用者自選指標 → 過度設計，不符合當前需求。

### 決策 2：標題以 SVG text 元素內嵌於地圖

**選擇**：在 `drawCounties()` 和 `drillDown()` 中，於 SVG `<g>` 內新增 `<text>` 元素，定位於左上角。移除 HTML 的 `.page-header` 區塊。

**理由**：SVG text 元素隨地圖 viewBox 自動縮放，保持響應式行為。以半透明背景矩形搭配確保文字在地圖上的可讀性。

**替代方案**：使用 CSS `position: absolute` overlay → 需額外處理響應式定位問題，且與 SVG viewBox 的縮放行為不一致。

### 決策 3：CSS 變數驅動的暗色模式

**選擇**：
1. 在 `style.css` 新增 `[data-theme="dark"]` 選擇器覆寫 `:root` 變數
2. 使用 `prefers-color-scheme: dark` media query 作為預設值
3. 在 `common.js` 新增切換邏輯，將使用者偏好存入 `localStorage`
4. 在導覽列新增切換按鈕

**理由**：CSS 變數方案不需引入額外依賴，且所有現有元件已使用 CSS 變數，切換主題時自動生效。`localStorage` 確保重整頁面後偏好不遺失。

**替代方案**：
- 獨立的 `dark.css` 檔案 → 增加 HTTP 請求，且需同步維護兩份樣式
- CSS `filter: invert()` → 圖片與地圖色彩會被反轉，效果不佳

## Risks / Trade-offs

- **[風險] 地圖色彩在暗色模式下對比度不足** → 暗色模式下調整地圖背景色與邊框色，確保 Choropleth 色彩可辨識
- **[風險] SVG 內嵌文字在小螢幕上過小** → 使用相對於 viewBox 的字體大小，並設定合理的最小值
- **[取捨] 暗色模式切換會觸發整頁重繪** → 因為使用 CSS 變數，瀏覽器原生處理重繪效率高，可接受
