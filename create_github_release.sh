#!/bin/bash
# GitHub Release Uploader for v3.0

echo "Creating GitHub Release v3.0 with all assets..."

# Check if files exist
echo "Checking release files..."

LINUX_PACKAGE="dist/RegenerativeAddressesPro_v3.0_Linux.tar.gz"
WINDOWS_PACKAGE="RegenerativeAddressesPro_v3.0_Windows_Package.zip"
RELEASE_NOTES="RELEASE_NOTES_v3.0.md"

if [ ! -f "$LINUX_PACKAGE" ]; then
    echo "Error: Linux package not found: $LINUX_PACKAGE"
    exit 1
fi

if [ ! -f "$WINDOWS_PACKAGE" ]; then
    echo "Error: Windows package not found: $WINDOWS_PACKAGE"
    exit 1
fi

if [ ! -f "$RELEASE_NOTES" ]; then
    echo "Error: Release notes not found: $RELEASE_NOTES"
    exit 1
fi

echo "All release files found!"

# Create release using curl (requires GitHub token)
echo "To complete the GitHub release, visit:"
echo "https://github.com/LilToreyFTW/deathdub/releases/new"
echo ""
echo "Release Information:"
echo "Tag: v3.0"
echo "Target: master"
echo "Title: Regenerative Addresses Tool Pro v3.0 - Professional Security Protection"
echo ""
echo "Assets to upload:"
echo "- $LINUX_PACKAGE ($(du -h $LINUX_PACKAGE | cut -f1))"
echo "- $WINDOWS_PACKAGE ($(du -h $WINDOWS_PACKAGE | cut -f1))"
echo ""
echo "Release Notes: Use content from $RELEASE_NOTES"
echo ""
echo "Manual Steps:"
echo "1. Go to https://github.com/LilToreyFTW/deathdub/releases/new"
echo "2. Enter v3.0 as tag"
echo "3. Select master as target"
echo "4. Enter title: Regenerative Addresses Tool Pro v3.0 - Professional Security Protection"
echo "5. Copy content from RELEASE_NOTES_v3.0.md"
echo "6. Upload both release assets"
echo "7. Publish release"

# Display file sizes
echo ""
echo "File Details:"
ls -lh $LINUX_PACKAGE $WINDOWS_PACKAGE $RELEASE_NOTES
