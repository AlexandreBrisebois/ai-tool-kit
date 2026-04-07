# 🎨 Favicon Generation Skill

This skill allows an agent to generate a full set of web-ready favicons from a single high-resolution source image (PNG).

## 🧠 Reasoning Instructions
1. **Source Discovery**: Identify a high-resolution source image (PNG). The tool will auto-detect `favicon.png`, `logo.png`, or `master-favicon.png` in the current directory if no path is provided.
2. **Directory Management**: Decide on the output directory. Defaults to the current directory (`.`). Use `--yes` if specifying a new path to ensure it's created.
3. **Execution**: Run the `tools/favicon/generate.sh` script.
4. **Validation**: Use `--json` to verify that all assets were created successfully.

## 🛠️ Tool Interaction
- **Path**: `tools/favicon/generate.sh`
- **Primary Command**: `./generate.sh --json --yes [source] [target]`
- **Minimal Command**: `./generate.sh` (uses auto-detection and current dir)

## 📝 Example Scenarios
- **Scenario A (Auto)**: "Generate favicons for this project."
  - Agent: Checks for `favicon.png`, finds it, runs `tools/favicon/generate.sh --json`.
- **Scenario B (Explicit)**: "Use assets/branding/logo-512.png for favicons and put them in public/."
  - Agent: Runs `tools/favicon/generate.sh --json --yes assets/branding/logo-512.png public/`.

## 📋 Requirements
- **Python 3.14**: The bootstrap script handles venv creation, but Python 3.14 must be installed on the system.
