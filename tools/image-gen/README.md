# 🖼️ Gemini Image Generator Tool

An agent-ready tool for generating high-quality images using Google's Gemini/Imagen models, featuring a customizable vision-based critique and retry loop.

## ⚙️ Configuration

The tool requires a Google API Key. You can provide this via an environment variable or a `.env` file in the tool's directory.

1.  Copy `.env.example` to `.env`.
2.  Add your `GOOGLE_API_KEY`.

## 🚀 Usage

```bash
python tools/image-gen/generator.py [options] [prompt_or_markdown_file]
```

### Options
- `-o, --output`: Destination path (default: `output/generated.webp`).
- `-j, --json`: Machine-readable JSON output of process and critique.
- `-c, --critique`: Specific critique instructions (as text) or a path to a critique file.
- `--no-critique`: Skip the vision feedback loop.
- `-f, --force`: Overwrite existing files.

### 🎨 Critique Hierarchy
The tool automatically determines critique criteria in the following order:
1.  **Explicit Flag**: `-c, --critique "[criteria]"`
2.  **Project Config**: A local `critique.md` file in the working directory.
3.  **Default Logic**: Evaluates image accuracy and quality against the original prompt.

### Examples
#### Text Prompt
```bash
python tools/image-gen/generator.py "A futuristic cityscape, neon-noir style" -o assets/cityscape.webp
```

#### Custom Critique File
```bash
python tools/image-gen/generator.py "Futuristic terminal icon" -c my_aesthetic.md -o output/icon.webp
```

#### From Markdown (Frontmatter)
If a markdown file is provided, the tool parses its frontmatter for an `image_prompt` key.
```bash
python tools/image-gen/generator.py content/docs/features.md -o static/images/features.webp
```

## 🛠️ Implementation Notes
- **Language**: Python 3
- **Dependencies**: `pyyaml`, `python-dotenv`, `requests`
- **Critique Loop**: Uses `gemini-1.5-flash` for high-speed image validation. If the initial result is rejected, it automatically retries once with the provided feedback.
