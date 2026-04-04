## 1. 投影計算最佳化

- [x] 1.1 修改 `static/js/map.js` 的 `createProjection()` 函式，新增選用參數以支援「排除指定縣市後計算 fitSize」。在 `drawCounties()` 呼叫時傳入排除金門縣、連江縣的 features 作為 fitSize 基準，但仍使用完整 projection 繪製所有縣市。驗收：台灣本島在 SVG 中明顯放大，佔據大部分可視區域

## 2. 離島位置偏移

- [x] 2.1 在 `drawCounties()` 中，繪製完所有 path 後，對 COUNTYNAME 為「金門縣」與「連江縣」的路徑元素施加 SVG `transform: translate(dx, dy)`，將其平移至台灣本島左下方區域。驗收：金門縣與連江縣顯示於地圖左下角附近
- [x] 2.2 在偏移後的離島周圍繪製虛線矩形框（`stroke-dasharray`），標示該區域為位置調整後的離島。驗收：離島區域有虛線框圍繞
- [x] 2.3 確認偏移後的離島仍保有 mouseover tooltip 與 click drillDown 互動功能。驗收：懸停顯示 tooltip，點擊可進入鄉鎮視圖

## 3. 測試與驗證

- [x] 3.1 重啟 Docker container，在瀏覽器中驗證：本島放大、離島位於左下角虛線框內、tooltip 與下鑽功能正常。驗收：三項功能均正常運作
