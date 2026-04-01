#!/bin/bash
# Linux Launcher for Regenerative Addresses Tool Pro v3.0

echo "Starting Regenerative Addresses Tool Pro v3.0..."
echo "Professional Security Protection Tool"
echo "=================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXECUTABLE="$SCRIPT_DIR/RegenerativeAddressesPro.exe"

# Check if executable exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "Error: Executable not found at $EXECUTABLE"
    echo "Please ensure the tool is properly built."
    exit 1
fi

# Check if executable is executable
if [ ! -x "$EXECUTABLE" ]; then
    echo "Making executable..."
    chmod +x "$EXECUTABLE"
fi

# Set environment variables
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export LD_LIBRARY_PATH="$SCRIPT_DIR/lib:$LD_LIBRARY_PATH"

# Run the executable
echo "Launching Regenerative Addresses Tool Pro..."
"$EXECUTABLE"

# Check exit status
if [ $? -eq 0 ]; then
    echo "Tool exited successfully."
else
    echo "Tool exited with error code: $?"
fi
