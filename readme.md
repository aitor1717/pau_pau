# Pau Pau — Modular Autonomous AI Agent

Pau Pau is a command-line orchestrator that interprets natural language and executes local Python tools, or writes them from scratch if needed. It can run self-generated scripts, and improve iteratively based on feedback. Designed for clarity, control, and autonomy.

## Features

- Local tool discovery and invocation based on language input
- Tool generation (code + manifest) through prompt-driven development
- Executes subprocesses with input validation and logging
- JSON-only structured communication for deterministic behavior
- GPT-4o native but model-agnostic

## Setup

- Install requirements
- Set OpenAI API key in the config file

## Example Commands

    Create a tool that checks CPU memory usage

    Create a the JSON file for the tool

    Run that tool

    Read the output file

    Write a new file from input

    Edit a tool and regenerate its manifest

    Log results and self-improve

Pau Pau works best when treated as a system-level assistant for modular automation and orchestration. It does not aim to chat. It acts.
