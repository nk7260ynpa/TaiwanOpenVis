## ADDED Requirements

### Requirement: 系統偏好自動偵測

系統 SHALL 在使用者首次造訪時，根據作業系統的色彩偏好設定（`prefers-color-scheme`）自動套用對應主題。

#### Scenario: 系統偏好為暗色模式

- **WHEN** 使用者首次造訪且作業系統設定為暗色模式
- **THEN** 網站自動套用暗色主題

#### Scenario: 系統偏好為亮色模式

- **WHEN** 使用者首次造訪且作業系統設定為亮色模式
- **THEN** 網站自動套用亮色主題

### Requirement: 使用者偏好持久化

系統 SHALL 將使用者手動選擇的主題偏好儲存於 `localStorage`，後續造訪時 MUST 優先使用已儲存的偏好，覆寫系統偏好。

#### Scenario: 偏好持久化

- **WHEN** 使用者手動切換主題後重新整理頁面
- **THEN** 頁面載入時套用使用者上次手動選擇的主題

#### Scenario: 清除偏好回歸系統預設

- **WHEN** 使用者清除瀏覽器 localStorage
- **THEN** 下次造訪時回歸系統偏好自動偵測

### Requirement: 地圖暗色模式相容

地圖 Choropleth 色彩 SHALL 在暗色模式下維持足夠對比度。地圖邊框與背景色 MUST 配合暗色主題調整。

#### Scenario: 暗色模式下地圖可讀性

- **WHEN** 使用者在暗色模式下瀏覽地圖頁面
- **THEN** 地圖區塊邊框使用深色描邊，Choropleth 色彩在暗色背景上清晰可辨
