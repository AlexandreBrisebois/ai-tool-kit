# 🧪 MLX-LM Manager Tool

Manage local LLMs on Apple Silicon (M-series chips). Supports downloading, starting an OpenAI-compatible server, stopping, and listing models.

## ⚙️ Configuration

The tool can be configured via environment variables or a `.env` file in the tool's directory.

1.  Copy `.env.example` to `.env`.
2.  (Optional) Set `MLX_LM_MODEL_PATH` to your preferred models directory (defaults to `./models`).

## 🚀 Usage

The easiest way to run the MLX-LM manager is via the provided bootstrap script, which automatically manages the Python virtual environment for you.

```bash
./mlx-lm.sh [command] [options]
```

### Commands
- `download [model_id]`: Download a model from HuggingFace (e.g. `mlx-community/phi-4-4b`).
- `start [model_id_or_path]`: Start the server on a specified port.
- `stop`: Stop the currently running server.
- `list`: List all locally available models.

### Options
- `--port, -p`: Custom port (default: 8080).
- `--json, -j`: Output result as machine-readable JSON.

### Examples
#### Running Phi-4 Locally
```bash
./mlx-lm.sh download mlx-community/phi-4-4b
./mlx-lm.sh start mlx-community/phi-4-4b --port 8080
```

## 🛠️ Implementation Notes
- **Language**: Python 3
- **Optimized**: Native Apple Silicon acceleration via MLX.
- **API**: Provides an OpenAI-compatible endpoint at `http://localhost:8080/v1`.
