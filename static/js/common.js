/**
 * TaiwanOpenVis 共用工具函式。
 */

/**
 * 呼叫後端 API 並回傳 JSON。
 * @param {string} path - API 路徑（如 "/api/population/counties"）。
 * @returns {Promise<any>} 回傳的 JSON 資料。
 */
async function fetchAPI(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`API 錯誤: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

/**
 * 將數字格式化為千分位。
 * @param {number} num - 要格式化的數字。
 * @returns {string} 格式化後的字串。
 */
function formatNumber(num) {
  return num.toLocaleString("zh-TW");
}

/**
 * 初始化導覽列的漢堡選單切換。
 */
function initNavbar() {
  const toggle = document.querySelector(".navbar-toggle");
  const links = document.querySelector(".navbar-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      links.classList.toggle("open");
    });
  }
}

document.addEventListener("DOMContentLoaded", initNavbar);
