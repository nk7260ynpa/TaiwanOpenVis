## ADDED Requirements

### Requirement: 暗色模式主題變數

系統 SHALL 在 CSS 中定義暗色主題的色彩變數，當 `[data-theme="dark"]` 屬性套用於 `<html>` 元素時，所有 CSS 變數 MUST 切換為暗色主題對應值。

#### Scenario: 暗色模式色彩套用

- **WHEN** `<html>` 元素的 `data-theme` 屬性設為 `"dark"`
- **THEN** 頁面背景、文字、卡片、導覽列等元件 SHALL 使用暗色主題配色

### Requirement: 導覽列主題切換按鈕

系統 SHALL 在導覽列中提供主題切換按鈕，允許使用者手動切換亮色/暗色模式。

#### Scenario: 點擊切換按鈕

- **WHEN** 使用者點擊導覽列中的主題切換按鈕
- **THEN** 頁面主題在亮色與暗色之間切換，按鈕圖示同步更新
