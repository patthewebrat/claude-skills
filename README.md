# Claude Code Skills

A collection of custom skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Available Skills

| Category | Skills |
|----------|--------|
| [FreeScout](./freescout/) | Helpdesk integration skills for retrieving tickets and conversations |

## Installation

Skills can be installed at the user level or project level:

### User-Level Installation

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/claude-skills/<skill-folder> ~/.claude/skills/<skill-name>
```

### Project-Level Installation

```bash
mkdir -p .claude/skills
ln -s /path/to/claude-skills/<skill-folder> .claude/skills/<skill-name>
```

## Structure

Each skill category has its own directory with:

- `README.md` - Category overview and setup instructions
- Individual skill folders containing:
  - `SKILL.md` - Skill definition and trigger conditions
  - `scripts/` - Supporting scripts and tools

## Contributing

To add a new skill:

1. Create a new category folder or use an existing one
2. Add a skill folder with `SKILL.md` defining the skill behavior
3. Include any necessary scripts in a `scripts/` subdirectory
4. Update the category README with setup instructions
5. Update this README to list the new skill category

## License

MIT
