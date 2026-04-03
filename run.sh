#!/bin/bash
# 啟動 TaiwanOpenVis Docker container。

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly IMAGE_NAME="taiwan-open-vis"
readonly CONTAINER_NAME="taiwan-open-vis"

# 停止並移除既有的 container
if docker ps -aq -f name="${CONTAINER_NAME}" | grep -q .; then
  echo "停止既有 container..."
  docker rm -f "${CONTAINER_NAME}" > /dev/null 2>&1
fi

# 建立 image
bash "${SCRIPT_DIR}/docker/build.sh"

echo "啟動 container: ${CONTAINER_NAME}..."
docker run -d \
  --name "${CONTAINER_NAME}" \
  -p 8000:8000 \
  -v "${SCRIPT_DIR}/data:/app/data" \
  -v "${SCRIPT_DIR}/logs:/app/logs" \
  "${IMAGE_NAME}"

echo "服務已啟動: http://localhost:8000"
