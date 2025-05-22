from pathlib import Path
import json
import subprocess
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

    result = subprocess.check_output(["python", str(target_path)], stderr=subprocess.STDOUT, text=True)
    print(f"[execute_file output]\n{result}")

except subprocess.CalledProcessError as e:
    print(f"[ERROR in file execution]\n{e.output}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
