# 🛠️ Tool Creation Recipe (Agent Guide)

This recipe is the standard for building reliable, agentic tools within this repository. Follow these steps to ensure every tool is high-quality, maintainable, and "agent-ready".

---

## 1. Spec-First Design
Before writing code, create a specification in `.specs/name.spec.md`.
- **Goal**: Clear intent (What it does, What it doesn't do).
- **Inputs**: Required/Optional flags, environment variables.
- **Outputs**: Expected standard output (JSON preferred).

## 2. Core Implementation Rules
Every tool *must* adhere to these 5 constraints:
1. **Non-Interactive**: No user prompts. Use `--yes` or `-f` for bypass.
2. **Machine-Readable**: Implement a `-j` or `--json` flag for all outputs.
3. **Self-Documenting**: Robust `--help` that explains all flags and shows examples.
4. **Environment First**: Secrets MUST be pulled from `.env` or system variables.
5. **Atomic**: One tool, one specific job. Pipe-friendly output.

## 3. Bundled Tool Structure
Each tool implementation resides in `tools/tool-name/` and includes its own skill definition.
```text
tools/tool-name/
├── main.py or tool.sh    # Main executable
├── SKILL.md              # Reasoning instructions (with YAML frontmatter)
├── tool-spec.json        # Structured JSON spec for agent tool-calling
├── requirements.txt      # Dependencies (if Python)
└── README.md             # Usage guide and agent notes
```

## 4. Universal Skill Standards
- **`SKILL.md`**: Must start with YAML frontmatter (`name`, `description`). Use relative paths (e.g., `./tool.sh`) for interaction.
- **`tool-spec.json`**: Follow the OpenAI/OpenAPI function calling schema.

## 5. Verification
Every tool must be tested with:
- `tool --help` (Does it explain correctly?)
- `tool [action] --json` (Is the output valid JSON?)
- `tool [destructive] --yes` (Does it skip prompts?)
