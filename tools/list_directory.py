from pathlib import Path
import json
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
INPUT_PATH = SCRIPT_DIR / "input.json"

try:
    with open(INPUT_PATH, encoding="utf-8") as f:
        params = json.load(f)

    directory = params.get("directory", "")
    target_path = ROOT_DIR / directory

    if not target_path.exists() or not target_path.is_dir():
        raise ValueError(f"Invalid directory: {target_path}")

    items = [str(p.name) for p in target_path.iterdir()]
    print(json.dumps(items, indent=2))

except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
