# 🖼️ Gemini Image Generation Skill

This skill allows an agent to generate images using Gemini/Imagen models, with an optional vision-based critique loop to ensure high-quality results that match specific criteria.

## 🧠 Reasoning Instructions
1. **Prompt Resolution**: If a markdown file is provided, it is parsed for frontmatter (e.g., `image_prompt`). Otherwise, the provided text is used directly.
2. **Critique Logic**: By default, a vision-based critique loop is active. You can customize the critique criteria using the following hierarchy:
   - **Explicit**: Pass a specific critique prompt via the `--critique` flag.
   - **Local Config**: Create a `critique.md` file in the current working directory to define persistent project aesthetics.
   - **Default**: If neither is provided, the tool evaluates the image against the original prompt for accuracy and quality.
3. **Refinement**: If the critique fails, the tool automatically attempts a second generation using the feedback provided by the vision model.
4. **Secret Management**: Ensure `GOOGLE_API_KEY` is present in the environment or `.env`.

## 🛠️ Tool Interaction
- **Path**: `tools/image-gen/generator.py`
- **Primary Command**: `python tools/image-gen/generator.py --json "[prompt]" --output "[path]"`
- **Custom Critique**: `python tools/image-gen/generator.py --critique "[criteria_or_file]" ...`

## 📝 Example Scenario
**User**: "Generate a futuristic city terminal icon."
**Agent Activity**:
1. Check if a local `critique.md` exists to understand the project's visual style.
2. Run `python tools/image-gen/generator.py --json "Futuristic city terminal icon, isometric, neon accents" --output assets/icons/terminal.webp`.
3. If the critique fails, the tool handles the retry automatically.
4. Inform the user of the saved path and include the critique feedback if relevant.
