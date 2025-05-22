from pathlib import Path
import json
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
INPUT_PATH = SCRIPT_DIR / "input.json"

def validate_params(params):
    required = ["base", "filename", "content"]
    for key in required:
        if key not in params:
            raise ValueError(f"Missing required input: {key}")
    if not isinstance(params["base"], str) or not isinstance(params["filename"], str):
        raise TypeError("Base and filename must be strings.")
    if not isinstance(params["content"], str):
        raise TypeError("Content must be a string.")
    if "subfolder" in params and not isinstance(params["subfolder"], str):
        raise TypeError("Subfolder must be a string if provided.")

try:
    with open(INPUT_PATH, encoding="utf-8") as f:
        params = json.load(f)

    validate_params(params)

    base = params["base"]
    subfolder = params.get("subfolder", "")
    filename = params["filename"]
    content = params["content"]
    dry_run = params.get("dry_run", False)

    target_path = ROOT_DIR / base / subfolder / filename
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        print(f"[Dry run] Would create: {target_path}")
        print(f"[Dry run] Content:\n{content}")
    else:
        target_path.write_text(content, encoding="utf-8")
        print(f"File created at: {target_path}")

except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
