# 🧪 MLX-LM Local LLM Manager Specification

## Goal
Manage and interact with local Large Language Models (LLMs) optimized for Apple Silicon using the `mlx-lm` library.

## Functional Requirements

### 1. Download Model
- Input: HuggingFace model repo ID (e.g. `mlx-community/phi-4-4b`).
- Output: Download status and local path.
- **`--json`**: Return download progress/path as JSON.

### 2. Start Server
- Input: Local model path or repo ID.
- Behavior: Start an OpenAI-compatible server on a specific port (default `8080`).
- **`--json`**: Return server status and API endpoint.
- **`--port`**: Custom port selection.
- **`--detached`**: Run in background (save PID for stopping).

### 3. Stop Server
- Input: PID or port numbers.
- Behavior: Terminate the running server.
- **`--json`**: Return termination status.

### 4. List Models
- Behavior: List all MLX-compatible models currently downloaded in the `models/` directory.
- **`--json`**: Return list as JSON.

## Recommended Models (Apple Silicon Optimized) with quantizations
- **Phi-4**: `mlx-community/phi-4-4b`
- **Gemma 4 (26B)**: `mlx-community/gemma-4-26b-it-4bit`

## Technical Architecture
- Use **`mlx-lm`** directly via Python for maximum performance.
- Avoid Docker for this tool to maximize "Bare Metal" acceleration of the Unified Memory Architecture (UMA) on M-series chips.
- Wrap the Python library into a robust CLI.

## Success Criteria (JSON Output)
```json
{
  "status": "server_started",
  "model": "mlx-community/gemma-4-26b-it-4bit",
  "endpoint": "http://localhost:8080/v1",
  "pid": 12345
}
```
