#!/usr/bin/env python3
"""
🛠️ AI Tool Kit: Gemini Image Generator
=====================================
A project-agnostic tool for high-quality image generation with vision-based critique.
"""

import argparse
import base64
import json
import os
import pathlib
import re
import sys
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_IMAGE_MODEL_PREFERENCE = [
    "gemini-3-pro-image-preview",
    "imagen-4.0-generate-001",
    "imagen-3.0-generate-002",
]

# ---------------------------------------------------------------------------
# Utility Functions (Minimal Replacements for content_automation)
# ---------------------------------------------------------------------------

def http_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def parse_frontmatter(content: str):
    import yaml
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)), match.group(2)
    return {}, content

# ---------------------------------------------------------------------------
# Core Logic
# ---------------------------------------------------------------------------

def generate_image(prompt: str, model="gemini-3-pro-image-preview") -> Optional[bytes]:
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    try:
        response = http_json(url, payload)
        for part in response.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"])
    except Exception as e:
        print(f"[ERROR] API failed: {e}", file=sys.stderr)
    return None

def critique_image(img_bytes: bytes, prompt: str, critique_instructions: Optional[str] = None) -> Dict[str, Any]:
    b64_img = base64.b64encode(img_bytes).decode("utf-8")
    
    # Define the critique prompt based on provided instructions or default
    if critique_instructions:
        critique_prompt = f"""Evaluate this generated image against these specific criteria:
{critique_instructions}

Context of the original prompt: {prompt}
Return JSON only: {{"keep": true|false, "feedback": "reasoning"}}"""
    else:
        critique_prompt = f"""Evaluate this generated image against the following prompt.
Prompt: {prompt}
Audit criteria: Ensure the image accurately reflects the prompt and is of high visual quality.
Return JSON only: {{"keep": true|false, "feedback": "reasoning"}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"text": critique_prompt},
                {"inline_data": {"mime_type": "image/webp", "data": b64_img}}
            ]
        }]
    }

    try:
        result = http_json(url, payload)
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group())
    except Exception as e:
        return {"keep": True, "feedback": f"Critique error: {e}"}
    return {"keep": True, "feedback": "No feedback parsed."}

def main():
    parser = argparse.ArgumentParser(description="AI Tool Kit: Gemini Image Generator")
    parser.add_argument("prompt_or_file", help="The text prompt or path to a markdown file.")
    parser.add_argument("--output", "-o", default="output/generated.webp", help="Save path.")
    parser.add_argument("--json", "-j", action="store_true", help="Format output as JSON.")
    parser.add_argument("--critique", "-c", help="Specific critique instructions or path to a critique file.")
    parser.add_argument("--no-critique", action="store_true", help="Skip vision critique.")
    parser.add_argument("--force", "-f", action="store_true", help="Overwrite existing files.")

    args = parser.parse_args()

    if not API_KEY:
        print(json.dumps({"status": "error", "message": "API Key Missing"}) if args.json else "[ERROR] GOOGLE_API_KEY required.")
        sys.exit(1)

    # 1. Resolve Prompt
    prompt = args.prompt_or_file
    if os.path.isfile(prompt):
        with open(prompt, 'r') as f:
            fm, _ = parse_frontmatter(f.read())
            prompt = fm.get("image_prompt") or prompt

    # 2. Output Check
    output_path = pathlib.Path(args.output)
    if not args.force and output_path.exists():
        if args.json:
            print(json.dumps({"status": "error", "message": "Output exists, use --force"}))
            sys.exit(1)
        else:
            print(f"[WARN] {output_path} exists. Aborted.")
            sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 3. Generation
    if not args.json: print(f"[INFO] Generating image for: {prompt[:50]}...")
    
    img_bytes = generate_image(prompt)
    if not img_bytes:
        sys.exit(1)

    # 4. Critique Hierarchy
    critique = {"keep": True, "feedback": "Skipped"}
    if not args.no_critique:
        critique_instructions = None
        
        # 1. Check --critique argument (could be a string or a file path)
        if args.critique:
            if os.path.isfile(args.critique):
                with open(args.critique, 'r') as f:
                    critique_instructions = f.read()
            else:
                critique_instructions = args.critique
        
        # 2. Check for local critique.md if no instructions provided yet
        if not critique_instructions and os.path.exists("critique.md"):
            with open("critique.md", 'r') as f:
                critique_instructions = f.read()

        if not args.json: print("[INFO] Critiquing image...")
        critique = critique_image(img_bytes, prompt, critique_instructions)
        
        if not critique["keep"]:
            if not args.json: print(f"[RETRY] Redoing with feedback: {critique['feedback']}")
            img_bytes = generate_image(f"{prompt}\n\nRevision: {critique['feedback']}")

    # 5. Save
    output_path.write_bytes(img_bytes)

    # 5. Result
    if args.json:
        print(json.dumps({
            "status": "success",
            "file": str(output_path),
            "critique": critique
        }, indent=2))
    else:
        print(f"[SUCCESS] Image saved to {output_path}")

if __name__ == "__main__":
    main()
