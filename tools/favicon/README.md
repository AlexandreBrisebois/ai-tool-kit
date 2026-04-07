# 🎨 Favicon Generator

A robust tool for generating a complete set of web-ready favicon assets from a single high-resolution source image.

## 🚀 Usage

The Favicon generator is a self-contained Python script powered by **`uv`**. It automatically manages its own dependencies (Pillow) and Python version (>= 3.14).

### Running the Tool
From the tool directory:
```bash
./generator.py [source] [output_dir] [options]
```

From the project root:
```bash
uv run tools/favicon/generator.py [source] [output_dir] [options]
```

### Examples
```bash
# Basic usage (auto-detects favicon.png or logo.png)
./generator.py

# Specify source and output directory
./generator.py my-logo.png ./static

# Output as JSON for agent integration
./generator.py my-logo.png ./dist --json --yes
```

## ⚙️ How it Works

1.  **Engine**: [uv](https://docs.astral.sh/uv/) (Zero-config execution).
2.  **Generation**: The core logic in `generator.py` uses **Pillow** to perform high-quality resizing (LANCZOS).
3.  **Assets**: It generates:
    - `favicon-16x16.png`
    - `favicon-32x32.png`
    - `apple-touch-icon.png` (180x180)
    - `android-chrome-192x192.png`
    - `android-chrome-512x512.png`
    - `favicon.ico` (Multi-resolution: 16x16, 32x32, 48x48)

## 📋 Requirements

- **uv**: Required for execution.
- **Python 3.14+**: Automatically managed and downloaded by `uv` if needed.
