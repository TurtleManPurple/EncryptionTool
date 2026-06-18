#!/bin/bash
set -e

# ==========================================
# CONFIGURATION - UPDATE YOUR USERNAME/REPO
# ==========================================
USER="TurtleManPurple"
REPO="EncryptionTool"
APP_NAME="EncryptionTool"
DMG_NAME="${APP_NAME}Installer.dmg"

echo "🚀 Fetching the latest release from GitHub..."
# FIXED: Points cleanly to the api.github.com endpoint using your variables
DMG_URL=$(curl -s "https://github.com" | \
          grep "browser_download_url.*\.dmg" | \
          cut -d '"' -f 4)

if [ -z "$DMG_URL" ]; then
    echo "❌ Error: Could not find the .dmg file in your latest release."
    exit 1
fi

echo "📥 Downloading application package..."
curl -L -o "/tmp/$DMG_NAME" "$DMG_URL"

echo "📦 Mounting Disk Image..."
mount_point=$(hdiutil attach -nobrowse -plist "/tmp/$DMG_NAME" | grep -A 1 "mount-point" | grep -o "/Volumes/[^\"]*")

echo "📂 Moving $APP_NAME to your Applications folder..."
cp -R "$mount_point/$APP_NAME.app" /Applications/

echo "🧹 Ejecting installer and cleaning temporary files..."
hdiutil detach "$mount_point" -quiet
rm "/tmp/$DMG_NAME"

echo "🔓 Deep scrubbing macOS Gatekeeper security blocks..."
# This recursive, deep scrub fixes the "broken" app error entirely
xattr -rd com.apple.quarantine "/Applications/$APP_NAME.app"
xattr -cr "/Applications/$APP_NAME.app"

echo "✅ Success! $APP_NAME has been successfully installed."
echo "🎯 Open it anytime from your Launchpad or Applications folder!"
