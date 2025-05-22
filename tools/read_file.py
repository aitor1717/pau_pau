from pathlib import Path
import json
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
INPUT_PATH = SCRIPT_DIR / "input.json"

try:
    with open(INPUT_PATH, encoding="utf-8") as f:
        params = json.load(f)

    if "path" not in params or not isinstance(params["path"], str):
        raise ValueError("Missing or invalid 'path' parameter.")

    target_path = ROOT_DIR / params["path"]
    if not target_path.exists():
        raise FileNotFoundError(f"File not found: {target_path}")

    content = target_path.read_text(encoding="utf-8")
    print(f"[read_file output]\n{content}")

except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
