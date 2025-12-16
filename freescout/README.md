# FreeScout Skills for Claude Code

Claude Code skills for interacting with FreeScout helpdesk.

## Available Skills

| Skill | Description |
|-------|-------------|
| [ticket-retriever](./ticket-retriever/) | Retrieve and display FreeScout ticket conversations |

## Setup

### 1. Configure FreeScout Connection

Create `~/.freescout/config.json`:

```json
{
  "url": "support.example.com",
  "api_key": "your-api-key-here",
  "mailbox_id": 1
}
```

**Configuration fields:**
- `url` - Your FreeScout instance URL (without https://)
- `api_key` - API key from FreeScout (Manage > API Keys)
- `mailbox_id` - Default mailbox ID to use

### 2. Install Skills

Symlink the skill folders to your Claude Code skills directory:

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Symlink the ticket-retriever skill
ln -s /path/to/claude-skills/freescout/ticket-retriever ~/.claude/skills/freescout-ticket-retriever
```

Or for project-level installation:

```bash
mkdir -p .claude/skills
ln -s /path/to/claude-skills/freescout/ticket-retriever .claude/skills/freescout-ticket-retriever
```

### 3. Get Your FreeScout API Key

1. Log in to your FreeScout instance as an admin
2. Go to **Manage** > **API Keys**
3. Click **New API Key**
4. Give it a name (e.g., "Claude Code")
5. Copy the generated key to your config file

## Usage

Once installed, Claude will automatically use these skills when you:

- Ask to look up a ticket: "Get FreeScout ticket 123"
- Reference a ticket number: "What's the status of #456?"
- Want to review a conversation: "Show me the conversation for ticket 789"

## Requirements

- Python 3.6+
- FreeScout with API module enabled
- Valid API key with read permissions
