# AI Tool Kit 🛠️

A collection of agent-optimized tools and skills for Apple Silicon. Built in public for [srvrlss.dev](https://srvrlss.dev).

## 🚀 Overview

This repository provides a standardized framework for building and using AI-ready tools. Each tool is designed to be **non-interactive**, **machine-readable**, and **self-documenting**, making them ideal for both developers and AI agents (Claude Code, GitHub Copilot, Gemini CLI, etc.).

## 📂 Repository Structure

- **[`.specs/`](./.specs)**: Functional requirements and design specifications (Spec-First).
- **[`tools/`](./tools)**: Core implementations, executables, and tool-specific guides.
- **[`skills/`](./skills)**: Universal agent instructions and structured tool-calling specs.
- **[`recipes/`](./recipes)**: Standard workflows for tool creation and repository maintenance.

## ⚡ Quick Start: AI Skill Sync

To allow AI agents (Gemini CLI, Claude Code, GitHub Copilot) to discover and use the skills in this repository, run the synchronization script. 

> [!NOTE]
> This synchronization is for **AI Agent Skill discovery** only. You can still run all tools in the `tools/` directory directly using Bash or Python regardless of whether you run this script.

### 1. Sync Skills
Run the following command to add project-local skill paths to your global AI tool configurations:

```bash
# Sync all supported agents (Gemini, Claude, Copilot)
./manage-env.sh --install all

# Or sync a specific agent
./manage-env.sh --install gemini
```

| Tool | Sync Method | Local Path | Description |
| :--- | :--- | :--- | :--- |
| **Gemini / Antigravity** | `gemini skills link` | `./tools/*` | Links each tool directory as a skill. |
| **Claude Code** | `.clauderc` | `./claude/` | Native project-root discovery. |
| **GitHub Copilot CLI** | `copilot-instructions.md` | `./tools/*` | Adds repo-level instructions for Copilot. |

### 2. Manual VS Code Setup
For **VS Code**, programmatic updates to `settings.json` are brittle. Please manually add the absolute path of the `tools/` directory to your VS Code settings if your AI extension supports custom instruction paths.

## 🛠️ Tools & Skills

Each tool is "bundled" with its own **`SKILL.md`** and **`tool-spec.json`**, allowing AI agents to understand and execute it directly from the tool's directory.

| Tool | Description | Status | Agent Skill |
| :--- | :--- | :--- | :--- |
| **[Favicon Gen](./tools/favicon)** | Generate a complete web-ready favicon set from a single image. | 🚧 In Progress | [Link](./tools/favicon/SKILL.md) |
| **[Image Gen](./tools/image-gen)** | Gemini 3.1 Pro powered image generation with a vision critique loop. | 🚧 In Progress | [Link](./tools/image-gen/SKILL.md) |

## 📦 Getting Started

This repository uses a **zero-config execution model** powered by **`uv`**. Each tool manages its own dependencies and Python version (>= 3.14) automatically.

1. **Install `uv`**:
   If you don't have it, install it via Homebrew:
   ```bash
   brew install uv
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/AlexandreBrisebois/ai-tool-kit.git
   cd ai-tool-kit
   ```

3. **Choose a tool**:
   Navigate to a tool's directory in `tools/`.
   ```bash
   cd tools/image-gen
   ```

4. **Configure Environment**:
   If the tool requires an API key or custom paths, copy its local `.env.example` to `.env`.
   ```bash
   cp .env.example .env
   ```

5. **Run the Tool**:
   All tools are executable and will handle their own setup on the first run.
   ```bash
   ./generator.py --help
   ```

## 🏗️ Building New Tools

To maintain consistency, please follow the [**Tool Creation Recipe**](./recipes/tool-creation.md) when adding new capabilities.


---
Built by [Alexandre Brisebois](https://srvrlss.dev)

