/**
 * TaiwanOpenVis 資料詳情頁邏輯。
 */

(function () {
  "use strict";

  const countyTitle = document.getElementById("countyTitle");
  const countySummary = document.getElementById("countySummary");
  const tableBody = document.querySelector("#townTable tbody");
  const tableHeaders = document.querySelectorAll("#townTable th");

  let townData = [];
  let sortKey = "population";
  let sortAsc = false;

  /** 從 URL 取得縣市名稱。 */
  function getCountyFromURL() {
    const parts = window.location.pathname.split("/");
    return decodeURIComponent(parts[parts.length - 1]);
  }

  /** 排序並渲染表格。 */
  function renderTable() {
    const sorted = [...townData].sort((a, b) => {
      const va = a[sortKey];
      const vb = b[sortKey];
      if (typeof va === "string") {
        return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
      }
      return sortAsc ? va - vb : vb - va;
    });

    tableBody.innerHTML = sorted
      .map(
        (t) => `
        <tr>
          <td>${t.town}</td>
          <td>${formatNumber(t.households)}</td>
          <td>${formatNumber(t.male)}</td>
          <td>${formatNumber(t.female)}</td>
          <td>${formatNumber(t.population)}</td>
        </tr>`
      )
      .join("");

    // 更新排序箭頭
    tableHeaders.forEach((th) => {
      const arrow = th.querySelector(".sort-arrow");
      if (arrow) arrow.remove();
      if (th.dataset.key === sortKey) {
        const span = document.createElement("span");
        span.className = "sort-arrow";
        span.textContent = sortAsc ? "▲" : "▼";
        th.appendChild(span);
      }
    });
  }

  /** 初始化欄位排序事件。 */
  function initSort() {
    tableHeaders.forEach((th) => {
      th.addEventListener("click", () => {
        const key = th.dataset.key;
        if (sortKey === key) {
          sortAsc = !sortAsc;
        } else {
          sortKey = key;
          sortAsc = key === "town";
        }
        renderTable();
      });
    });
  }

  /** 載入資料。 */
  async function init() {
    const county = getCountyFromURL();
    countyTitle.textContent = county;

    try {
      townData = await fetchAPI(`/api/population/towns/${encodeURIComponent(county)}`);

      const totalPop = townData.reduce((sum, t) => sum + t.population, 0);
      const totalHH = townData.reduce((sum, t) => sum + t.households, 0);
      countySummary.textContent =
        `共 ${townData.length} 個鄉鎮市區，` +
        `總人口 ${formatNumber(totalPop)}，` +
        `總戶數 ${formatNumber(totalHH)}`;

      initSort();
      renderTable();
    } catch (err) {
      countyTitle.textContent = "載入失敗";
      countySummary.textContent = err.message;
    }
  }

  init();
})();
