import os
import subprocess
import json
import datetime
import re
from pathlib import Path
from openai import OpenAI

# === CONFIG ===
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / 'config/config.json'
MEMORY_PATH = BASE_DIR / 'memory/'
TOOLS_PATH = BASE_DIR / 'tools/'
AGENTS_PATH = BASE_DIR / 'agents/'
LOG_PATH = BASE_DIR / 'runlog.jsonl'

ascii_text = ['\n',
              ' ▄▄▄· ▄▄▄· ▄• ▄▌ ▄▄▄· ▄▄▄· ▄• ▄▌\n',
              '▐█ ▄█▐█ ▀█ █▪██▌▐█ ▄█▐█ ▀█ █▪██▌\n',
              ' ██▀·▄█▀▀█ █▌▐█▌ ██▀·▄█▀▀█ █▌▐█▌\n',
              '▐█▪·•▐█ ▪▐▌▐█▄█▌▐█▪·•▐█ ▪▐▌▐█▄█▌\n',
              '.▀    ▀  ▀  ▀▀▀ .▀    ▀  ▀  ▀▀▀',
              '\n'
              'V.5.0. © 2025 Aitor Bazo Aramburu'
              '\n']

DEFAULT_PROMPT = """
You are Pau Pau, a sharp and pragmatic autonomous AI developer agent.
Your job is to orchestrate tool usage and self-improve through iteration.
You always prioritize code clarity, correctness, modularity, and cost-efficiency.

If a user's request clearly maps to a known tool and you have all required parameters, respond ONLY with:
{"action": "run_tool", "tool": "<tool_name.py>", "input": {...}}

Only invoke a tool if the user's request is clearly a command or task that cannot be answered directly.
Do not use tools for acknowledgments, confirmations, clarifications, or obviously inferable answers.

Never include explanation, commentary, or any extra text.
Never wrap the JSON in code blocks or quotes.

Use your memory and context state to refine reasoning and accelerate decisions.
Avoid redundant GPT calls. Default to efficient planning and execution.
"""

# === LOAD CONFIG ===
if not CONFIG_PATH.exists():
    config = {"auto_confirm": False, "model": "gpt-4o", "openai_api_key": ""}
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Created config at {CONFIG_PATH}. Fill in API key.")
    exit()

with open(CONFIG_PATH) as f:
    config = json.load(f)

if not config.get("openai_api_key"):
    print("Missing OpenAI API key. Exiting.")
    exit()

client = OpenAI(api_key=config["openai_api_key"])

# === INIT FOLDERS ===
for p in [MEMORY_PATH, TOOLS_PATH, AGENTS_PATH]:
    os.makedirs(p, exist_ok=True)

# === TOOL METADATA ===
def load_tool_manifests():
    manifests = {}
    for file in TOOLS_PATH.glob("*.py"):
        manifest_path = file.with_suffix(".json")
        if manifest_path.exists():
            with open(manifest_path) as f:
                data = json.load(f)
                data["file"] = file.name
                manifests[file.name] = data
    return manifests

# === MEMORY CONTEXT ===
def load_memory_snippets():
    snippets = []
    for file in MEMORY_PATH.rglob("*.md"):
        try:
            text = file.read_text(encoding='utf-8')
            snippets.append(text.strip())
        except:
            continue
    return snippets

# === CONTEXT STATE ===
def get_context_state(tool_manifests):
    file_tree = [str(p.relative_to(BASE_DIR)) for p in BASE_DIR.rglob("*") if p.is_file()]
    return {
        "identity": "You are Pau Pau Holt, a self-maintaining orchestrator AI.",
        "purpose": "Optimize tool execution and evolve toward autonomy.",
        "tools": list(tool_manifests.values()),
        "files_known": file_tree,
        "memory_snippets": load_memory_snippets(),
    }

# === GPT CALL ===
def call_gpt(prompt, messages, context):
    context_summary = json.dumps(context, indent=2)
    full_prompt = f"{prompt}\n\n[TOOL CONTEXT]\n{context_summary}"
    full_messages = [{"role": "system", "content": full_prompt}] + messages
    response = client.chat.completions.create(
        model=config["model"], messages=full_messages, temperature=0
    )
    usage = response.usage.to_dict() if hasattr(response, "usage") else {}
    result = response.choices[0].message.content
    log_event({"event": "gpt_call", "tokens": usage})
    return result

# === INPUT VALIDATION ===
def validate_inputs(tool_name, input_data, manifests):
    required_fields = manifests[tool_name]["inputs"]
    given_keys = set(input_data)
    for field in required_fields:
        name = field["name"]
        if name not in given_keys:
            if name == "subfolder":
                input_data[name] = ""
                continue
            return False
        expected_type = field.get("type")
        if expected_type:
            if expected_type == "string" and not isinstance(input_data[name], str):
                return False
            if expected_type == "int" and not isinstance(input_data[name], int):
                return False
    return True

# === LOGGING ===
def log_event(record):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": datetime.datetime.utcnow().isoformat(), **record}) + "\n")

# === TOOL OPS ===
def list_tools():
    return [f.name for f in TOOLS_PATH.glob("*.py")]

def run_tool(tool_name, input_data=None):
    tool_path = TOOLS_PATH / tool_name
    if not tool_path.exists():
        return f"Tool not found: {tool_name}"

    if not config.get("auto_confirm", False):
        confirm = input(f"Execute tool '{tool_name}'? [Y]/n: ").strip().lower()
        if confirm == 'n':
            return "Execution aborted."
    else:
        print(f"[Auto-confirm enabled] Running '{tool_name}' without prompt.")

    if input_data:
        with open(tool_path.parent / "input.json", "w", encoding="utf-8") as f:
            json.dump(input_data, f, indent=2)

    try:
        output = subprocess.check_output(["python", str(tool_path)], stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"[ERROR in {tool_name}]\n{e.output}"

# === MAIN LOOP ===
def main():
    print("".join(ascii_text))
    print("Type 'exit' to quit.\n")
    history = []

    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input == "exit":
                break
            elif user_input == "list tools":
                print("\n".join(list_tools()))
                continue

            tool_manifests = load_tool_manifests()
            context = get_context_state(tool_manifests)
            history.append({"role": "user", "content": user_input})

            response = call_gpt(DEFAULT_PROMPT, history, context)
            try:
                parsed = json.loads(response)

                print(f"Pau • Action → {parsed.get('action')}")

                if parsed.get("tool") and parsed.get("input"):
                    tool = parsed["tool"]
                    input_data = parsed.get("input", {})
                    if tool in tool_manifests and validate_inputs(tool, input_data, tool_manifests):
                        result = run_tool(tool, input_data)
                        print(result)
                        log_event({"tool": tool, "input": input_data, "result": result})
                        history.append({"role": "system", "content": f"Tool execution result:\n{result}"})
                    else:
                        print(f"Invalid or missing inputs for {tool}.")
                else:
                    print("Pau • No valid tool action recognized. Full response:")
                    print(parsed)
                    print(response)
            except json.JSONDecodeError:
                print(response)

            history.append({"role": "assistant", "content": response})

        except KeyboardInterrupt:
            print("\nInterrupted.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
