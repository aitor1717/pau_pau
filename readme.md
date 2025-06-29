# Pau Pau — Modular Self-Building AI Agent

![Grid](cover.png)

Pau Pau is a command-line orchestrator that interprets natural language and executes local Python tools, or writes them from scratch if needed. It can run self-generated scripts, and improve iteratively. Designed for clarity, control, and autonomy.

This project is the result of an obsession with AI agents. After getting lost in the guides and baffled by new architectures for agent networks, I decided to build a simple GPT wrapper with the key ability to read, write, and execute files locally. This simplification results in a clumsy CLI with unlimited potential for self-improvement. It can create and optimize its own memory architecture, produce QA tools for its own use, and read and improve its own main code.

The project is being put on hold for now. Since it’s in a very early stage, please consider adding security fallbacks before using it.

## Features

- Local tool discovery and invocation based on language input
- Tool generation (code + manifest) through prompt-driven development
- Executes subprocesses with input validation and logging
- JSON-only structured communication for deterministic behavior
- GPT-4o native but model-agnostic

## Setup

- Install requirements
- Set your OpenAI API key in `config/config.json`

## Example Functionality

    Create a tool that checks current CPU memory usage

    Generate a JSON manifest for the tool

    Run the tool and print results — no restart needed

    Create a file containing the output

    Edit an existing tool

    Log results and iterate

Pau Pau works best when treated as an assistant for modular automation. It does not aim to chat; it aims to act.
