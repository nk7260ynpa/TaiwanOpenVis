## ADDED Requirements

### Requirement: 縣市層級 Choropleth 地圖

系統 SHALL 在地圖頁面以 D3.js 繪製台灣縣市層級的 Choropleth 地圖，以色彩深淺呈現各縣市的人口數。地圖 MUST 使用 TopoJSON 格式的行政區邊界資料。

#### Scenario: 載入地圖頁面

- **WHEN** 使用者開啟地圖頁面（`/map`）
- **THEN** 頁面顯示台灣全島的縣市 Choropleth 地圖，各縣市依人口數填充不同深淺的顏色

#### Scenario: 地圖包含圖例

- **WHEN** 地圖渲染完成
- **THEN** 頁面顯示色彩圖例（legend），標示人口數的數值範圍與對應顏色

### Requirement: 縣市懸停互動

系統 SHALL 在使用者滑鼠懸停於縣市區塊時，顯示 tooltip 呈現該縣市的詳細資料。

#### Scenario: 滑鼠懸停顯示 tooltip

- **WHEN** 使用者將滑鼠移至某縣市區塊上方
- **THEN** 顯示 tooltip 包含：縣市名稱、總人口數、面積、人口密度

#### Scenario: 滑鼠移開隱藏 tooltip

- **WHEN** 使用者將滑鼠移離縣市區塊
- **THEN** tooltip 消失

### Requirement: 縣市下鑽至鄉鎮層級

系統 SHALL 支援使用者點擊縣市後，地圖切換顯示該縣市底下的鄉鎮市區 Choropleth 地圖。

#### Scenario: 點擊縣市進入鄉鎮視圖

- **WHEN** 使用者點擊地圖上的某縣市
- **THEN** 地圖以動畫縮放至該縣市範圍，顯示鄉鎮市區的 Choropleth 地圖，色彩依人口數填充

#### Scenario: 從鄉鎮視圖返回縣市視圖

- **WHEN** 使用者在鄉鎮視圖中點擊「返回全台」按鈕
- **THEN** 地圖以動畫縮放回全台縣市 Choropleth 視圖

### Requirement: 鄉鎮懸停互動

系統 SHALL 在鄉鎮視圖中，使用者滑鼠懸停於鄉鎮區塊時顯示 tooltip。

#### Scenario: 鄉鎮 tooltip 顯示

- **WHEN** 使用者在鄉鎮視圖中將滑鼠移至某鄉鎮區塊
- **THEN** 顯示 tooltip 包含：鄉鎮名稱、戶數、男性人口、女性人口、總人口

### Requirement: 響應式地圖

地圖 SHALL 根據瀏覽器視窗大小自動調整尺寸，確保在桌面與平板裝置上均可正常顯示。

#### Scenario: 視窗縮放時地圖自適應

- **WHEN** 使用者調整瀏覽器視窗大小
- **THEN** 地圖 SVG 自動縮放以填滿容器寬度，維持台灣地圖的正確比例

### Requirement: 地圖內嵌標題

系統 SHALL 在地圖 SVG 內部左上角顯示標題文字，以 overlay 方式呈現於地圖之上。標題 MUST 搭配半透明背景確保可讀性。

#### Scenario: 縣市視圖顯示標題

- **WHEN** 使用者開啟地圖頁面或從鄉鎮視圖返回全台視圖
- **THEN** 地圖 SVG 左上角顯示「台灣人口分佈地圖」主標題與「點擊縣市可查看鄉鎮市區的人口分佈」副標題

#### Scenario: 鄉鎮視圖顯示標題

- **WHEN** 使用者點擊縣市進入鄉鎮視圖
- **THEN** 地圖 SVG 左上角顯示該縣市名稱作為標題
