#!/usr/bin/env python3
"""
🎨 AI Tool Kit: Favicon Generator
================================
A Python-based favicon generator that creates a complete set of web-ready assets
using Pillow. Supports multi-resolution .ico files.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    from PIL import Image
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # This will be handled by the bootstrap script, but for CLI usage:
    print("[ERROR] Missing dependencies. Run through generate.sh or install Pillow and python-dotenv.")
    sys.exit(1)

# --- Configuration ---
S_16 = (16, 16)
S_32 = (32, 32)
S_48 = (48, 48)
S_180 = (180, 180)
S_192 = (192, 192)
S_512 = (512, 512)

DEFAULT_SOURCES = ["favicon.png", "logo.png", "master-favicon.png", "apple-touch-icon.png"]

def generate_favicons(source: str, output_dir: str, use_json: bool = False, auto_yes: bool = False) -> Dict[str, Any]:
    source_path = Path(source)
    target_dir = Path(output_dir)

    # 1. Validation
    if not source_path.exists():
        return {"status": "error", "message": f"Source file not found: {source}"}

    if not target_dir.exists():
        if auto_yes:
            target_dir.mkdir(parents=True, exist_ok=True)
        else:
            return {"status": "error", "message": f"Output directory does not exist: {output_dir}. Use --yes to create it."}

    try:
        with Image.open(source_path) as img:
            # Ensure square aspect ratio or at least handle it
            if img.width != img.height:
                if not use_json: print(f"[WARN] Source image is not square ({img.width}x{img.height}). Assets will be square-padded/resized.")

            generated_files = []

            # --- PNG Assets ---
            mapping = {
                f"favicon-{S_16[0]}x{S_16[1]}.png": S_16,
                f"favicon-{S_32[0]}x{S_32[1]}.png": S_32,
                "apple-touch-icon.png": S_180,
                f"android-chrome-{S_192[0]}x{S_192[1]}.png": S_192,
                f"android-chrome-{S_512[0]}x{S_512[1]}.png": S_512,
            }

            for filename, size in mapping.items():
                out_path = target_dir / filename
                # Use Resampling.LANCZOS for high quality
                resized = img.resize(size, Image.Resampling.LANCZOS)
                resized.save(out_path, "PNG")
                generated_files.append(filename)

            # --- ICO Asset (Multi-resolution) ---
            ico_path = target_dir / "favicon.ico"
            # Standard ico sizes: 16, 32, 48
            img.save(ico_path, format="ICO", sizes=[S_16, S_32, S_48])
            generated_files.append("favicon.ico")

            return {
                "status": "success",
                "source": str(source_path),
                "output_dir": str(target_dir),
                "files": generated_files
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description="AI Tool Kit: Favicon Generator")
    parser.add_argument("source", nargs="?", help="Path to high-resolution source PNG.")
    parser.add_argument("output_dir", nargs="?", default=".", help="Destination for assets.")
    parser.add_argument("--json", "-j", action="store_true", help="Output result as JSON.")
    parser.add_argument("--yes", "-y", action="store_true", help="Auto-create output directory.")
    
    args = parser.parse_args()

    # Auto-detection logic
    source_file = args.source
    if not source_file:
        for default in DEFAULT_SOURCES:
            if os.path.exists(default):
                source_file = default
                break
    
    if not source_file:
        error_msg = "Source file not specified and none of the defaults found: " + ", ".join(DEFAULT_SOURCES)
        if args.json:
            print(json.dumps({"status": "error", "message": error_msg}))
        else:
            print(f"[ERROR] {error_msg}")
        sys.exit(1)

    result = generate_favicons(source_file, args.output_dir, args.json, args.yes)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["status"] == "success":
            print(f"[SUCCESS] Favicons generated from {result['source']} into {result['output_dir']}")
            print("Files created: " + ", ".join(result["files"]))
        else:
            print(f"[ERROR] {result['message']}")
            sys.exit(1)

if __name__ == "__main__":
    main()
