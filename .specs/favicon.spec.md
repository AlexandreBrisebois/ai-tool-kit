# 🎨 Favicon Generator Specification

## Goal
Generate a complete, high-quality set of favicon assets for web projects from a single high-resolution source image. Optimized for macOS using native tools (`sips`).

## Inputs
- **Source Image**: A high-resolution (min 512x512) PNG file.
  - Default: Auto-detected if any of these exist in the current directory: `favicon.png`, `logo.png`, `master-favicon.png`.
  - Manual: Provided as the first positional argument.
- **Output Directory**: The destination for generated assets.
  - Default: `.` (Current Directory)
- **Flags**:
  - `--json`: Return output as a JSON object containing the list of generated files.
  - `--yes`: Automatically create the output directory if it does not exist (useful when specifying a custom path).

## Expected Outputs
The tool must generate the following standard formats:
- `favicon-16x16.png`
- `favicon-32x32.png`
- `apple-touch-icon.png` (180x180)
- `android-chrome-192x192.png`
- `android-chrome-512x512.png`
- `favicon.ico` (A copy of the 32x32 PNG)

## Success Criteria (JSON Output)
```json
{
  "status": "success",
  "source": "./{image-name}.png",
  "output_dir": "./favicons",
  "files": [
    "favicon-16x16.png",
    "favicon-32x32.png",
    "apple-touch-icon.png",
    "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    "favicon.ico"
  ]
}
```
