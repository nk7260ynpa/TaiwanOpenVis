## MODIFIED Requirements

### Requirement: 縣市層級 Choropleth 地圖

系統 SHALL 在地圖頁面以 D3.js 繪製台灣縣市層級的 Choropleth 地圖，以色彩深淺呈現各縣市的人口數。地圖 MUST 使用 TopoJSON 格式的行政區邊界資料。

#### Scenario: 載入地圖頁面

- **WHEN** 使用者開啟地圖頁面（`/map`）
- **THEN** 頁面顯示台灣全島的縣市 Choropleth 地圖，各縣市依人口數填充不同深淺的顏色

#### Scenario: 地圖包含圖例

- **WHEN** 地圖渲染完成
- **THEN** 頁面顯示色彩圖例（legend），標示人口數的數值範圍與對應顏色

## ADDED Requirements

### Requirement: 地圖內嵌標題

系統 SHALL 在地圖 SVG 內部左上角顯示標題文字，以 overlay 方式呈現於地圖之上。標題 MUST 搭配半透明背景確保可讀性。

#### Scenario: 縣市視圖顯示標題

- **WHEN** 使用者開啟地圖頁面或從鄉鎮視圖返回全台視圖
- **THEN** 地圖 SVG 左上角顯示「台灣人口分佈地圖」主標題與「點擊縣市可查看鄉鎮市區的人口分佈」副標題

#### Scenario: 鄉鎮視圖顯示標題

- **WHEN** 使用者點擊縣市進入鄉鎮視圖
- **THEN** 地圖 SVG 左上角顯示該縣市名稱作為標題
