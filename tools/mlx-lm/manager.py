#!/usr/bin/env python3
"""
🛠️ AI Tool Kit: MLX-LM Manager
==============================
Start, stop, and download local LLMs on Apple Silicon.
"""

import argparse
import json
import os
import pathlib
import signal
import subprocess
import sys
import time
from typing import List, Optional

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Configuration ---
DEFAULT_MODELS_DIR = pathlib.Path(os.getenv("MLX_LM_MODEL_PATH", "./models"))
PID_FILE = pathlib.Path("/tmp/mlx_lm_server.pid")

def get_installed_models() -> List[str]:
    """List directories in the models folder."""
    if not DEFAULT_MODELS_DIR.exists():
        return []
    return [d.name for d in DEFAULT_MODELS_DIR.iterdir() if d.is_dir()]

def download_model(model_id: str):
    """Download a model from HuggingFace using mlx-lm library."""
    # We use subprocess to call the CLI version for easier progress tracking
    cmd = [sys.executable, "-m", "mlx_lm.server", "--model", model_id, "--dry-run"] # Dry run just downloads
    print(f"[INFO] Downloading {model_id}...")
    subprocess.run(cmd)

def start_server(model_path: str, port: int = 8080):
    """Start the MLX-LM server."""
    if PID_FILE.exists():
        print("[ERROR] Server already appears to be running (PID file exists).")
        return

    cmd = [
        sys.executable, "-m", "mlx_lm.server",
        "--model", model_path,
        "--port", str(port)
    ]
    
    print(f"[INFO] Starting server for {model_path} on port {port}...")
    # Start process in background
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))
    
    print(f"[SUCCESS] Server started with PID {process.pid}")

def stop_server():
    """Stop the running MLX-LM server."""
    if not PID_FILE.exists():
        print("[ERROR] No PID file found. Server might not be running.")
        return

    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())

    try:
        os.kill(pid, signal.SIGTERM)
        print(f"[INFO] Stopping server (PID {pid})...")
        time.sleep(2)
        if PID_FILE.exists():
            PID_FILE.unlink()
        print("[SUCCESS] Server stopped.")
    except ProcessLookupError:
        print("[WARN] Process not found. Cleaning up PID file.")
        PID_FILE.unlink()

def main():
    parser = argparse.ArgumentParser(description="MLX-LM Local LLM Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Download
    dl_parser = subparsers.add_parser("download", help="Download a model from HuggingFace")
    dl_parser.add_argument("model_id", help="HF Repo ID (e.g. mlx-community/phi-4)")

    # Start
    start_parser = subparsers.add_parser("start", help="Start the server")
    start_parser.add_argument("model", help="Model ID or local path")
    start_parser.add_argument("--port", "-p", type=int, default=8080, help="Port to serve on")

    # Stop
    subparsers.add_parser("stop", help="Stop the running server")

    # List
    subparsers.add_parser("list", help="List downloaded models")

    # Global flags
    parser.add_argument("--json", "-j", action="store_true", help="Output result as JSON")

    args = parser.parse_args()

    if args.command == "download":
        download_model(args.model_id)
        if args.json:
            print(json.dumps({"status": "downloaded", "model": args.model_id}))

    elif args.command == "start":
        start_server(args.model, args.port)
        if args.json:
            print(json.dumps({"status": "started", "model": args.model, "port": args.port}))

    elif args.command == "stop":
        stop_server()
        if args.json:
            print(json.dumps({"status": "stopped"}))

    elif args.command == "list":
        models = get_installed_models()
        if args.json:
            print(json.dumps({"models": models}))
        else:
            print("Installed Models:")
            for m in models:
                print(f" - {m}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
