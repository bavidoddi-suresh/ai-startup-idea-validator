#!/bin/bash
# Deploy AI Startup Idea Validator to Hugging Face Spaces
#
# Usage:
#   ./deploy_to_hf.sh <your-hf-username>
#
# Prerequisites:
#   1. A Hugging Face account (https://huggingface.co/join)
#   2. Create a Space at https://huggingface.co/new-space
#      - Space name: ai-startup-idea-validator
#      - SDK: Docker
#      - Visibility: Public
#   3. Create an HF access token at https://huggingface.co/settings/tokens
#      (with "write" permission)

set -e

HF_USERNAME="${1:-}"

if [ -z "$HF_USERNAME" ]; then
    echo "Usage: ./deploy_to_hf.sh <your-huggingface-username>"
    echo ""
    echo "Before running this script:"
    echo "  1. Go to https://huggingface.co/new-space"
    echo "  2. Create a Space named 'ai-startup-idea-validator'"
    echo "  3. Select SDK: Docker"
    echo "  4. Set visibility: Public"
    echo "  5. Create an access token at https://huggingface.co/settings/tokens"
    exit 1
fi

SPACE_NAME="ai-startup-idea-validator"
SPACE_REPO="https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"
TEMP_DIR=$(mktemp -d)

echo "================================================"
echo "Deploying to Hugging Face Spaces"
echo "  Space: ${SPACE_REPO}"
echo "  Temp dir: ${TEMP_DIR}"
echo "================================================"

echo ""
echo "Step 1: Cloning HF Space repo..."
git clone "${SPACE_REPO}" "${TEMP_DIR}/space"

echo ""
echo "Step 2: Copying project files..."
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

cp "${SOURCE_DIR}/gradio_app.py" "${TEMP_DIR}/space/"
cp "${SOURCE_DIR}/Dockerfile" "${TEMP_DIR}/space/"
cp "${SOURCE_DIR}/requirements.txt" "${TEMP_DIR}/space/"
cp "${SOURCE_DIR}/pyproject.toml" "${TEMP_DIR}/space/"
cp -r "${SOURCE_DIR}/app" "${TEMP_DIR}/space/"

# Remove files that shouldn't go to HF
rm -rf "${TEMP_DIR}/space/app/.env"
rm -rf "${TEMP_DIR}/space/app/frontend"
rm -rf "${TEMP_DIR}/space/app/__pycache__"
find "${TEMP_DIR}/space" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "Step 3: Creating HF Spaces README..."
cat > "${TEMP_DIR}/space/README.md" << 'READMEEOF'
---
title: AI Startup Idea Validator
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: true
---

# AI Startup Idea Validator

Test your startup/business idea with AI. Enter your idea and the system will:

- **Find competitors** already doing something similar
- **Point out their weaknesses** (user complaints, missing features)
- **Suggest a unique value proposition** to help you compete
- **Score viability** (0-100) with risk assessment

## How to Use

1. Get a free Google AI Studio API key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Paste your API key in the field below
3. Type your startup idea and hit Enter
4. Wait 3-8 minutes for the full 6-stage analysis

## Pipeline

| Stage | Agent | What It Does |
|-------|-------|-------------|
| 1 | Market Research | Validates market size, growth, demographics |
| 2 | Competitor Mapping | Discovers competitors and their weaknesses |
| 3 | Gap Analysis | Quantitative scoring with Python code |
| 4 | Strategy Advisor | Crafts value proposition, 0-100 score |
| 5 | Report Generator | McKinsey/BCG-style HTML exec deck |
| 6 | Infographic | Shareable visual summary |

Built with [Google ADK](https://google.github.io/adk-docs/) and Gemini.
READMEEOF

echo ""
echo "Step 4: Pushing to Hugging Face..."
cd "${TEMP_DIR}/space"
git add -A
git commit -m "Deploy AI Startup Idea Validator"
git push

echo ""
echo "================================================"
echo "✅ Deployment complete!"
echo ""
echo "Your app will be live at:"
echo "  ${SPACE_REPO}"
echo ""
echo "It may take 2-5 minutes for the Docker image to build."
echo "================================================"

# Cleanup
rm -rf "${TEMP_DIR}"
