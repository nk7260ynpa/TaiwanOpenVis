#!/bin/bash
# 建立 TaiwanOpenVis Docker image。

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
readonly IMAGE_NAME="taiwan-open-vis"

echo "建立 Docker image: ${IMAGE_NAME}..."
docker build \
  -t "${IMAGE_NAME}" \
  -f "${SCRIPT_DIR}/Dockerfile" \
  "${PROJECT_DIR}"

echo "Docker image 建立完成: ${IMAGE_NAME}"
