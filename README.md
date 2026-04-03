# TaiwanOpenVis

台灣公開資料視覺化專案，將台灣政府公開資料透過互動式圖表呈現，讓使用者能直觀地探索與理解資料。

## 技術棧

- **後端**：Python（FastAPI, Pandas）
- **前端**：HTML/CSS/JavaScript（D3.js）
- **部署**：Docker

## 專案架構

```
TaiwanOpenVis/
├── docker/           # Docker 相關設定
│   ├── build.sh      # 建立 Docker image
│   ├── Dockerfile    # Docker image 定義
│   └── docker-compose.yaml  # （若需要）
├── openspec/         # OpenSpec 專案規格
│   ├── project.md    # 專案定義
│   ├── config.yaml   # OpenSpec 設定
│   ├── specs/        # 功能規格文件
│   └── changes/      # 變更紀錄
├── logs/             # 日誌檔案存放處
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
