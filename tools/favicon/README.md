# 🎨 Favicon Generator

A robust tool for generating a complete set of web-ready favicon assets from a single high-resolution source image.

## 🚀 Usage

The easiest way to run the Favicon generator is via the provided bootstrap script, which automatically manages the Python virtual environment for you.

```bash
# Basic usage (auto-detects favicon.png or logo.png)
./generate.sh

# Specify source and output directory
./generate.sh my-logo.png ./static

# Output as JSON for agent integration
./generate.sh --json --yes my-logo.png ./dist
```

## ⚙️ How it Works

1.  **Bootstrap**: `generate.sh` checks for Python 3.14 and sets up a local `.venv` if it doesn't exist.
2.  **Generation**: The core logic in `generator.py` uses **Pillow** to perform high-quality resizing (LANCZOS).
3.  **Assets**: It generates:
    - `favicon-16x16.png`
    - `favicon-32x32.png`
    - `apple-touch-icon.png` (180x180)
    - `android-chrome-192x192.png`
    - `android-chrome-512x512.png`
    - `favicon.ico` (Multi-resolution: 16x16, 32x32, 48x48)

## 📋 Requirements

- **macOS** (Optimized for Apple Silicon, though Python-based, it follows the project's macOS-first standards).
- **Python 3.14** (Required for the virtual environment).
