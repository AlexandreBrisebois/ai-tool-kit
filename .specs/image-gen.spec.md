# 🖼️ Gemini Image Generator Specification

## Goal
Generate images using the latest Gemini/Imagen models with an optional vision-based critique loop for high-quality results.

## Inputs
- **Prompt**: A text prompt for the image generation.
  - Can be a file path to a markdown file.

- **Output**: The path to save the generated image (default: `./generated.webp`). 
- **Flags**:
  - **`--json`**: Output process status and critique results as JSON.
  - **`--no-critique`**: Skip the vision-based feedback loop and save the first shot immediately.
  - **`--force`**: Overwrite existing files without asking.

## Expected Outputs
- A generated image (WebP or PNG).
- If `--json`: A JSON summary containing the final prompt used, critique feedback, and the output path.

## Secrets
- Requires **`GOOGLE_API_KEY`** from environment or `.env`.

## Success Criteria (JSON Output)
```json
{
  "status": "success",
  "prompt": "Minimalist digital landscape...",
  "critique": {
    "score": "PASS",
    "feedback": "Minimalist and abstract, no logos detected."
  },
  "file_path": "./generated.webp"
}
```
