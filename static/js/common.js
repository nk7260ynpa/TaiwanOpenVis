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

/**
 * 初始化主題：讀取 localStorage → 偵測系統偏好 → 套用。
 */
function initTheme() {
  const stored = localStorage.getItem("theme");
  if (stored) {
    document.documentElement.setAttribute("data-theme", stored);
  } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.documentElement.setAttribute("data-theme", "dark");
  }
  updateThemeIcon();
}

/**
 * 切換亮/暗主題並持久化至 localStorage。
 */
function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
  updateThemeIcon();
}

/**
 * 更新切換按鈕的圖示。
 */
function updateThemeIcon() {
  const btn = document.querySelector(".theme-toggle");
  if (!btn) return;
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  btn.textContent = isDark ? "\u2600\uFE0F" : "\uD83C\uDF19";
  btn.setAttribute("aria-label", isDark ? "切換亮色模式" : "切換暗色模式");
}

document.addEventListener("DOMContentLoaded", function () {
  initNavbar();
  initTheme();
});
