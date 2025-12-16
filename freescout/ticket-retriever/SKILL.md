---
name: freescout-ticket-retriever
description: Retrieve FreeScout support ticket conversations. Use when user asks to look up a FreeScout ticket, references a ticket number like #123, or wants to see a support conversation thread.
---

# FreeScout Ticket Retriever

Retrieves and displays FreeScout support ticket conversations with full thread history.

## When to Use

Use this skill when the user:
- Asks to look up a FreeScout ticket (e.g., "Get FreeScout ticket 123")
- References a ticket number (e.g., "What's happening with ticket #456?")
- Wants to review a support conversation
- Pastes a FreeScout conversation URL

## Prerequisites

The user must have configured `~/.freescout/config.json` with their FreeScout instance details. If the config is missing, inform them to create it with:

```json
{
  "url": "support.example.com",
  "api_key": "their-api-key",
  "mailbox_id": 1
}
```

## How to Retrieve a Ticket

1. Extract the ticket ID or number from the user's request
2. Run the fetch script:
   ```bash
   python3 /path/to/freescout/ticket-retriever/scripts/fetch_ticket.py <ticket_id>
   ```
3. Parse the JSON output and display it in the format below

## Output Format

Display the ticket conversation like this:

```markdown
## Ticket #[number]: [subject]
**Status:** [status] | **Assignee:** [assignee name or "Unassigned"] | **Customer:** [customer email]
**Created:** [created_at] | **Last Updated:** [updated_at]

---

### [sender_type] - [sender_name] ([created_at])
[message body]

---

### [sender_type] - [sender_name] ([created_at])
[message body]

[... continue for each thread]
```

## Example

User: "Look up FreeScout ticket 42"

1. Run: `python3 scripts/fetch_ticket.py 42`
2. Parse the JSON response
3. Display formatted conversation with all threads in chronological order

## Error Handling

- If config file is missing: Tell user to create `~/.freescout/config.json`
- If API returns error: Display the error message from the response
- If ticket not found: Inform user the ticket ID may be incorrect
