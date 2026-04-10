#!/bin/bash
# Download OpenSCAD AppImage if not already present
set -e

OPENSCAD_APPIMAGE="tools/openscad"
OPENSCAD_VERSION="2025.02.11"
OPENSCAD_URL="https://files.openscad.org/OpenSCAD-2021.01-x86_64.AppImage"

if [ -x "$OPENSCAD_APPIMAGE" ]; then
    echo "OpenSCAD AppImage already exists at $OPENSCAD_APPIMAGE"
    exec "$OPENSCAD_APPIMAGE" "$@"
fi

echo "OpenSCAD not found. Downloading AppImage to tools/..."
mkdir -p tools

if command -v wget >/dev/null 2>&1; then
    wget -O "$OPENSCAD_APPIMAGE" "$OPENSCAD_URL"
elif command -v curl >/dev/null 2>&1; then
    curl -L -o "$OPENSCAD_APPIMAGE" "$OPENSCAD_URL"
else
    echo "ERROR: Neither wget nor curl found. Please install one." >&2
    exit 1
fi

chmod +x "$OPENSCAD_APPIMAGE"
echo "OpenSCAD AppImage downloaded successfully."

# If called with arguments, execute openscad with them
if [ $# -gt 0 ]; then
    exec "$OPENSCAD_APPIMAGE" "$@"
fi
