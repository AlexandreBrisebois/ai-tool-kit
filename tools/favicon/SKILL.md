---
name: favicon-gen
description: Generate a set of web-ready favicons from a high-resolution PNG.
---

# 🎨 Favicon Generation Skill

This skill allows an agent to generate a full set of web-ready favicons from a single high-resolution source image (PNG).

## 🧠 Reasoning Instructions
1. **Source Discovery**: Identify a high-resolution source image (PNG). The tool will auto-detect `favicon.png`, `logo.png`, or `master-favicon.png` in the current directory if no path is provided.
2. **Directory Management**: Decide on the output directory. Defaults to the current directory (`.`). Use `--yes` if specifying a new path to ensure it's created.
3. **Execution**: Run the `./generator.py` script (located in the same directory as this skill).
4. **Validation**: Use `--json` to verify that all assets were created successfully.

## 🛠️ Tool Interaction
- **Path**: `./generator.py`
- **Engine**: Powered by `uv` (Zero-config execution).
- **Primary Command**: `./generator.py --json --yes [source] [target]`
- **Minimal Command**: `./generator.py` (uses auto-detection and current dir)

## 📝 Example Scenarios
- **Scenario A (Auto)**: "Generate favicons for this project."
  - Agent: Checks for `favicon.png`, finds it, runs `./generator.py --json`.
- **Scenario B (Explicit)**: "Use assets/branding/logo-512.png for favicons and put them in public/."
  - Agent: Runs `./generator.py --json --yes assets/branding/logo-512.png public/`.

## 📋 Requirements
- **uv**: Required for zero-config execution.
- **Python 3.14+**: Automatically managed by `uv`.
