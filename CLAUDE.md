# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains custom skills for Claude Code. Skills are modular capabilities that extend Claude Code's functionality through trigger-based activation.

## Skill Structure

Each skill follows this pattern:
- `SKILL.md` - Defines the skill name, description, trigger conditions, and usage instructions (YAML frontmatter + markdown body)
- `scripts/` - Supporting scripts that the skill invokes

Skills are organized by category (e.g., `freescout/ticket-retriever/`).

## Creating New Skills

1. Create a category folder if needed (e.g., `myservice/`)
2. Add a skill subfolder with `SKILL.md` containing:
   - YAML frontmatter with `name` and `description` (used for trigger matching)
   - Instructions for when/how to use the skill
   - Script invocation examples
3. Add supporting scripts in `scripts/` subdirectory
4. Update the category README with setup requirements

## Installation

Skills are symlinked into Claude Code's skills directory:

```bash
# User-level
ln -s /path/to/claude-skills/<category>/<skill> ~/.claude/skills/<skill-name>

# Project-level
ln -s /path/to/claude-skills/<category>/<skill> .claude/skills/<skill-name>
```

## Current Skills

### FreeScout Ticket Retriever
- **Path:** `freescout/ticket-retriever/`
- **Script:** `python3 scripts/fetch_ticket.py <ticket_id>`
- **Config:** `~/.freescout/config.json` with `url`, `api_key`, `mailbox_id`
- **Triggers:** ticket lookups, #123 references, FreeScout URLs
