# TaiwanOpenVis

台灣公開資料視覺化專案，將台灣政府公開資料轉化為互動式視覺化圖表。

## 專案架構

```
TaiwanOpenVis/
├── docker/           # Docker 相關設定
│   ├── build.sh      # 建立 Docker image
│   ├── Dockerfile    # Docker image 定義
│   └── docker-compose.yaml  # （若需要）
├── logs/             # 日誌檔案存放處
├── plan/             # 規格需求文件
├── run.sh            # 啟動主程式腳本
├── LICENSE           # Apache 2.0
└── README.md         # 專案說明
```

## 快速開始

### 建立 Docker Image

```bash
bash docker/build.sh
```

### 啟動服務

```bash
bash run.sh
```

## 授權條款

本專案採用 [Apache License 2.0](LICENSE) 授權。
