#!/bin/bash

# 🎨 AI Tool Kit: Favicon Generator Bootstrap Script
# ========================================
# This script ensures the local Python virtual environment is set up and
# correctly configured before running the Favicon generator.
#
# Usage:
#   ./generate.sh [source] [output_dir] [options] (e.g. ./generate.sh logo.png static/ --json)
#

# Stop on errors
set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/.venv"

# 0. 🔍 Check for Python 3.14
if ! command -v python3.14 &> /dev/null; then
    echo "❌ [ERROR] Python 3.14 not found. Please install it to use this tool."
    exit 1
fi

# 1. 🔧 Setup: Create virtual environment if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creating virtual environment with Python 3.14 in: $VENV_DIR"
    python3.14 -m venv "$VENV_DIR"
    
    echo "📦 Installing dependencies from requirements.txt..."
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
    echo "✅ Setup complete."
fi

# 2. 🚀 Execution: Execute the generator using the venv's Python
# Using absolute path to the venv's python ensures we use the correct one.
# We pass all arguments ("$@") to the generator.py script.
# We explicitly set the PYTHONPATH to the script directory to ensure module resolution.
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

"$VENV_DIR/bin/python" "$SCRIPT_DIR/generator.py" "$@"
