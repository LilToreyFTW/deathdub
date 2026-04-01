#!/bin/bash

# Simple Website Update Script
# Run this after updating the Regenerative Addresses Tool

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
V0_DIR="$SCRIPT_DIR/v0-regenerative-addresses-tool"

if [[ ! -d "$V0_DIR" ]]; then
    echo "❌ v0 website directory not found: $V0_DIR"
    exit 1
fi

log "Updating v0 website..."

cd "$V0_DIR"

# Get latest commit info from main repo
cd "$SCRIPT_DIR"
LATEST_COMMIT=$(git rev-parse HEAD)
COMMIT_COUNT=$(git rev-list --count HEAD)
SHORT_HASH=$(git rev-parse --short HEAD)

cd "$V0_DIR"

# Update version in header.tsx
sed -i "s/v[0-9]\+\.[0-9]\+\.[0-9]\+/v3.0.${COMMIT_COUNT}/g" components/header.tsx

# Update version in package.json
FULL_VERSION="v3.0.${COMMIT_COUNT}+${SHORT_HASH}"
sed -i "s/\"version\": \".*\"/\"version\": \"${FULL_VERSION}\"/g" package.json

success "Website updated to version $FULL_VERSION"

# Build the website
info "Building website..."
npm run build

success "Website built successfully!"

# Instructions for manual deployment
info "To deploy manually:"
echo "1. Push changes to GitHub:"
echo "   git add ."
echo "   git commit -m \"Update website to $FULL_VERSION\""
echo "   git push origin main"
echo ""
echo "2. Vercel will auto-deploy from GitHub"
echo ""
echo "3. Your websites will be updated at:"
echo "   - https://regenerative-addresses-tool.vercel.app"
echo "   - https://regenerative-addresses-t-git-2c19b3-coresremotehelpers-projects.vercel.app"
echo "   - https://regenerative-addresses-tool-lwpve9uqi.vercel.app"
