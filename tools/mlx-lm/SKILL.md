---
name: mlx_lm_manager
description: Download and manage local LLMs on Apple Silicon using MLX.
---

# 🧪 MLX-LM Management Skill

This skill allows an agent to download, start, stop, and list local LLMs optimized for Apple Silicon using the MLX framework.

## 🧠 Reasoning Instructions
1. **Model Discovery**: Use `list` to see which models are already available.
2. **Download**: If a requested model (e.g. `phi-4`) is missing, use `download` with the HF repo ID (e.g. `mlx-community/phi-4-4b`).
3. **Server Control**: Start the server on a specified port (default 8080) and keep track of the PID (managed by the tool).
4. **API Integration**: Once the server is "started", other agents can interact with it using the OpenAI-compatible API at `http://localhost:8080/v1`.

## 🛠️ Tool Interaction
- **Path**: `./manager.py`
- **Commands**:
  - `python ./manager.py --json list`
  - `python ./manager.py --json download [repo_id]`
  - `python ./manager.py --json start [model_id_or_path]`
  - `python ./manager.py --json stop`

## 📝 Example Scenario
**User**: "Run Phi-4 locally for me."
**Agent Activity**:
1. Check `list`. If `phi-4` is absent, run `python ./manager.py --json download mlx-community/phi-4-4b`.
2. Run `python ./manager.py --json start mlx-community/phi-4-4b`.
3. Provide the user with the local endpoint: `http://localhost:8080/v1`.
