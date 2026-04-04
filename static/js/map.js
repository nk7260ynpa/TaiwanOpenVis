/**
 * TaiwanOpenVis 地圖視覺化。
 *
 * 功能：
 * - 縣市層級 Choropleth 地圖（人口密度）
 * - 縣市懸停 tooltip
 * - 點擊縣市下鑽至鄉鎮視圖
 * - 鄉鎮懸停 tooltip
 * - 返回全台按鈕
 * - 響應式 SVG 縮放
 */

(function () {
  "use strict";

  const WIDTH = 800;
  const HEIGHT = 1000;

  const mapContainer = document.getElementById("mapContainer");
  const tooltipEl = document.getElementById("tooltip");
  const backBtn = document.getElementById("backBtn");
  const legendEl = document.getElementById("legend");

  let svg, g;
  let countiesGeo, townsGeo;
  let countyData = [];
  let townData = [];
  let currentView = "counties";

  /** 初始化 SVG。 */
  function initSVG() {
    svg = d3
      .select("#mapContainer")
      .append("svg")
      .attr("viewBox", `0 0 ${WIDTH} ${HEIGHT}`)
      .attr("preserveAspectRatio", "xMidYMid meet");

    g = svg.append("g");
  }

  /** 建立色彩比例尺。 */
  function createColorScale(data, valueKey) {
    const values = data.map((d) => d[valueKey]).filter((v) => v > 0);
    const max = d3.max(values);
    return d3
      .scaleSequential(d3.interpolateBlues)
      .domain([0, max]);
  }

  /** 繪製圖例。 */
  function drawLegend(colorScale, label) {
    legendEl.innerHTML = "";

    const steps = 6;
    const domain = colorScale.domain();
    const stepSize = (domain[1] - domain[0]) / steps;

    const lowLabel = document.createElement("span");
    lowLabel.textContent = "低";
    legendEl.appendChild(lowLabel);

    const bar = document.createElement("div");
    bar.className = "legend-bar";
    for (let i = 0; i < steps; i++) {
      const span = document.createElement("span");
      span.style.background = colorScale(domain[0] + stepSize * (i + 0.5));
      bar.appendChild(span);
    }
    legendEl.appendChild(bar);

    const highLabel = document.createElement("span");
    highLabel.textContent = "高";
    legendEl.appendChild(highLabel);

    const labelEl = document.createElement("span");
    labelEl.textContent = `（${label}）`;
    labelEl.style.marginLeft = "8px";
    legendEl.appendChild(labelEl);
  }

  /** 顯示 tooltip。 */
  function showTooltip(event, html) {
    tooltipEl.innerHTML = html;
    tooltipEl.classList.add("visible");
    tooltipEl.style.left = event.clientX + 24 + "px";
    tooltipEl.style.top = event.clientY - 28 + "px";
  }

  /** 隱藏 tooltip。 */
  function hideTooltip() {
    tooltipEl.classList.remove("visible");
  }

  /** 建立 D3 投影。 */
  function createProjection(geojson) {
    return d3.geoMercator().fitSize([WIDTH, HEIGHT], geojson);
  }

  /** 在 SVG 內部左上角繪製標題 overlay。 */
  function drawMapTitle(title, subtitle) {
    g.selectAll(".map-title-group").remove();
    const titleGroup = g.append("g").attr("class", "map-title-group");

    const padding = 12;
    const titleY = 36;
    const subtitleY = subtitle ? 60 : 0;

    // 半透明背景
    const bgRect = titleGroup
      .append("rect")
      .attr("class", "map-title-bg")
      .attr("x", 8)
      .attr("y", 8)
      .attr("rx", 6)
      .attr("ry", 6)
      .attr("fill", "var(--bg-card, #ffffff)")
      .attr("fill-opacity", 0.85);

    // 主標題
    const titleText = titleGroup
      .append("text")
      .attr("class", "map-title-text")
      .attr("x", 8 + padding)
      .attr("y", titleY)
      .attr("font-size", "22px")
      .attr("font-weight", "700")
      .attr("fill", "var(--text, #2d3748)")
      .text(title);

    let bgHeight = titleY + padding - 8;

    // 副標題
    if (subtitle) {
      titleGroup
        .append("text")
        .attr("class", "map-title-text")
        .attr("x", 8 + padding)
        .attr("y", subtitleY)
        .attr("font-size", "14px")
        .attr("fill", "var(--text-light, #718096)")
        .text(subtitle);
      bgHeight = subtitleY + padding - 8;
    }

    // 計算背景寬度
    const titleBBox = titleText.node().getBBox();
    const bgWidth = titleBBox.width + padding * 2;

    bgRect.attr("width", bgWidth).attr("height", bgHeight);
  }

  /** 繪製縣市 Choropleth。 */
  function drawCounties() {
    currentView = "counties";
    backBtn.classList.remove("visible");

    const countyLookup = new Map(
      countyData.map((d) => [d.county, d])
    );

    const geojson = topojson.feature(countiesGeo, countiesGeo.objects.counties);
    const projection = createProjection(geojson);
    const path = d3.geoPath().projection(projection);

    const colorScale = createColorScale(countyData, "population");
    drawLegend(colorScale, "人口數");

    g.transition().duration(500).attr("transform", "");

    g.selectAll("*").remove();
    g.selectAll("path")
      .data(geojson.features)
      .join("path")
      .attr("d", path)
      .attr("fill", (d) => {
        const info = countyLookup.get(d.properties.COUNTYNAME);
        return info ? colorScale(info.population) : "#ccc";
      })
      .attr("stroke", "#fff")
      .attr("stroke-width", 1)
      .style("cursor", "pointer")
      .on("mouseover", function (event, d) {
        d3.select(this).attr("stroke-width", 2).attr("stroke", "#333");
        const info = countyLookup.get(d.properties.COUNTYNAME);
        if (info) {
          showTooltip(
            event,
            `<strong>${info.county}</strong><br>` +
              `人口：${formatNumber(info.population)}<br>` +
              `面積：${formatNumber(info.area)} km²<br>` +
              `密度：${formatNumber(info.density)} 人/km²`
          );
        }
      })
      .on("mousemove", function (event) {
        tooltipEl.style.left = event.clientX + 24 + "px";
        tooltipEl.style.top = event.clientY - 28 + "px";
      })
      .on("mouseout", function () {
        d3.select(this).attr("stroke-width", 1).attr("stroke", "#fff");
        hideTooltip();
      })
      .on("click", function (event, d) {
        drillDown(d.properties.COUNTYNAME);
      });

    drawMapTitle("台灣人口分佈地圖", "點擊縣市可查看鄉鎮市區的人口分佈");
  }

  /** 下鑽至鄉鎮視圖。 */
  function drillDown(countyName) {
    currentView = "towns";
    backBtn.classList.add("visible");

    const towns = townData.filter((d) => d.county === countyName);
    if (towns.length === 0) return;

    const townLookup = new Map(towns.map((d) => [d.town, d]));

    const allTownsGeo = topojson.feature(
      townsGeo,
      townsGeo.objects.towns
    );
    const countyTowns = {
      type: "FeatureCollection",
      features: allTownsGeo.features.filter(
        (f) => f.properties.COUNTYNAME === countyName
      ),
    };

    const projection = createProjection(countyTowns);
    const path = d3.geoPath().projection(projection);

    const colorScale = createColorScale(towns, "population");
    drawLegend(colorScale, `${countyName} 鄉鎮人口`);

    g.selectAll("*").remove();
    g.selectAll("path")
      .data(countyTowns.features)
      .join("path")
      .attr("d", path)
      .attr("fill", (d) => {
        const info = townLookup.get(d.properties.TOWNNAME);
        return info ? colorScale(info.population) : "#ccc";
      })
      .attr("stroke", "#fff")
      .attr("stroke-width", 1)
      .attr("opacity", 0)
      .transition()
      .duration(500)
      .attr("opacity", 1);

    g.selectAll("path")
      .on("mouseover", function (event, d) {
        d3.select(this).attr("stroke-width", 2).attr("stroke", "#333");
        const info = townLookup.get(d.properties.TOWNNAME);
        if (info) {
          showTooltip(
            event,
            `<strong>${info.town}</strong><br>` +
              `戶數：${formatNumber(info.households)}<br>` +
              `男性：${formatNumber(info.male)}<br>` +
              `女性：${formatNumber(info.female)}<br>` +
              `總人口：${formatNumber(info.population)}`
          );
        }
      })
      .on("mousemove", function (event) {
        tooltipEl.style.left = event.clientX + 24 + "px";
        tooltipEl.style.top = event.clientY - 28 + "px";
      })
      .on("mouseout", function () {
        d3.select(this).attr("stroke-width", 1).attr("stroke", "#fff");
        hideTooltip();
      });

    drawMapTitle(countyName, "點擊鄉鎮可查看詳細資料");

    // 新增「查看詳情」連結
    const detailLink = document.createElement("a");
    detailLink.href = `/detail/${encodeURIComponent(countyName)}`;
    detailLink.className = "btn btn-outline";
    detailLink.textContent = "查看詳情";
    detailLink.style.marginLeft = "12px";
    backBtn.parentNode.insertBefore(detailLink, backBtn.nextSibling);
    detailLink.id = "detailLink";
  }

  /** 返回全台視圖。 */
  backBtn.addEventListener("click", function (e) {
    e.preventDefault();
    const detailLink = document.getElementById("detailLink");
    if (detailLink) detailLink.remove();
    drawCounties();
  });

  /** 載入所有資料並繪製地圖。 */
  async function init() {
    initSVG();

    const [countiesRes, townsRes, countyApi, townApi] = await Promise.all([
      d3.json("/static/data/taiwan-counties.topojson"),
      d3.json("/static/data/taiwan-towns.topojson"),
      fetchAPI("/api/population/counties"),
      fetchAPI("/api/population/towns/all").catch(() => null),
    ]);

    countiesGeo = countiesRes;
    townsGeo = townsRes;
    countyData = countyApi;

    // 如果有全部鄉鎮資料就用，否則留空（下鑽時再個別載入）
    if (townApi) {
      townData = townApi;
    }

    drawCounties();
  }

  init().catch((err) => {
    console.error("地圖初始化失敗:", err);
    mapContainer.innerHTML =
      '<p style="text-align:center;color:#e53e3e;padding:40px;">地圖載入失敗，請確認後端服務是否啟動。</p>';
  });
})();
