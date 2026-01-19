---
name: freescout-ticket-retriever
description: Retrieve FreeScout support ticket conversations. Use when user asks to look up a FreeScout ticket, references a ticket number like #123, or wants to see a support conversation thread.
---

# FreeScout Ticket Retriever

Retrieves and displays FreeScout support ticket conversations with full thread history. Can also push draft replies to tickets.

## When to Use

Use this skill when the user:
- Asks to look up a FreeScout ticket (e.g., "Get FreeScout ticket 123")
- References a ticket number (e.g., "What's happening with ticket #456?")
- Wants to review a support conversation
- Pastes a FreeScout conversation URL
- Asks to draft/write/push a reply to a ticket

## Prerequisites

The user must have configured `~/.freescout/config.json` with their FreeScout instance details:

```json
{
  "url": "support.example.com",
  "api_key": "your-api-key",
  "mailbox_id": 1,
  "user_id": 1,
  "first_name": "Patrick",
  "reply_style_prompt": "Optional: custom style instructions for draft replies"
}
```

**Required fields:**
- `url` - FreeScout instance URL
- `api_key` - API key from FreeScout
- `mailbox_id` - Mailbox ID
- `user_id` - Your FreeScout user ID (required for posting replies)
- `first_name` - Your first name (used for sign-off in replies)

**Optional fields:**
- `reply_style_prompt` - Custom style instructions that override the default prompt

## Retrieving a Ticket

1. Extract the ticket ID or number from the user's request
2. Run the fetch script:
   ```bash
   python3 ~/.claude/skills/freescout-ticket-retriever/scripts/fetch_ticket.py <ticket_id>
   ```
3. Parse the JSON output and display it in the format below

### Output Format

Display the ticket conversation like this:

```markdown
## Ticket #[number]: [subject]
**URL:** [url]
**Status:** [status] | **Assignee:** [assignee name or "Unassigned"] | **Customer:** [customer email]
**CC:** [comma-separated CC emails, or "None" if empty]
**Created:** [created_at] | **Last Updated:** [updated_at]

---

### [sender_type] - [sender_name] ([created_at])
[message body]

---

### [sender_type] - [sender_name] ([created_at])
[message body]

[... continue for each thread]
```

## Pushing a Draft Reply

When the user asks to draft, write, or push a reply to a ticket:

### Step 1: Determine the Ticket ID

1. If the user provides a ticket ID, use it
2. If no ticket ID is provided, look through the **current conversation context** for a previously retrieved ticket (from earlier use of this skill)
3. If still not found, ask the user for the ticket ID

### Step 2: Gather Context

Before generating the reply, ensure you have:
1. **Full ticket thread** - If not already in context, fetch it using the fetch script
2. **Session context** - Review what has been discussed, investigated, or fixed during this Claude session

### Step 3: Generate the Reply

1. Read `~/.freescout/config.json` to get the `first_name` for the sign-off and check for a custom `reply_style_prompt`
2. Generate a draft reply using the style prompt (custom if present, otherwise default below)
3. **Present a plain text preview** to the user (no HTML tags) for readability
4. Ask the user to sign off on the reply before proceeding

### Step 4: Get User Sign-Off

Display the draft reply as plain text and ask: "Does this look good to push as a draft?"

- If the user approves: proceed to Step 5
- If the user requests changes: make the changes and show updated preview
- Repeat until approved

### Step 5: Convert to HTML and Push

Once approved:
1. Convert the plain text reply to HTML format (applying formatting rules below)
2. Push to FreeScout as a draft

#### Default Style Prompt

```
Write a customer support reply following these guidelines:

FORMAT:
- Output as HTML (use <p> tags for paragraphs, <br> for line breaks)
- Use <ul> and <li> for bullet lists, <ol> and <li> for numbered lists
- Convert any URLs into clickable links: <a href="https://example.com">https://example.com</a>
- Do NOT include <html>, <head>, or <body> tags - just the content HTML

TONE & STYLE:
- Clear and concise - no waffle or unnecessary words
- British English spelling and phrasing
- Professional but friendly and approachable
- Written in layman's terms - avoid technical jargon unless the customer used it first
- Direct and to the point

STRUCTURE:
- Address the customer by their first name
- Acknowledge their issue briefly
- Explain what was found or done (if applicable)
- Provide clear next steps or resolution
- Keep it short - aim for 2-3 short paragraphs maximum
- ALWAYS end with the sign-off using the `first_name` from config:

<p><br>Kind regards,<br><br>{first_name from config}</p>

DO NOT:
- Use filler phrases like "I hope this email finds you well"
- Over-apologise
- Use corporate speak or buzzwords
- Include unnecessary pleasantries
- Use American spellings (use colour not color, organisation not organization, etc.)
```

#### Pushing the Draft

Run the push script with the HTML message. **Always include the CC recipients from the original ticket** using the `--cc` flag:

```bash
echo "Your HTML message here" | python3 ~/.claude/skills/freescout-ticket-retriever/scripts/push_draft.py <ticket_id> --stdin --cc "email1@example.com,email2@example.com"
```

Or directly:

```bash
python3 ~/.claude/skills/freescout-ticket-retriever/scripts/push_draft.py <ticket_id> --cc "email1@example.com,email2@example.com" "Your HTML message here"
```

**Important:** Always pass the CC recipients from the fetched ticket data to preserve the conversation's CC list.

### Step 6: Confirm to User

After pushing, inform the user:
- That the draft was created successfully
- Provide the URL to review: `https://[freescout-url]/conversation/[ticket_id]`
- Remind them to review and send when ready

## Error Handling

- If config file is missing: Tell user to create `~/.freescout/config.json`
- If `user_id` is missing: Inform user it's required for posting replies
- If API returns error: Display the error message from the response
- If ticket not found: Inform user the ticket ID may be incorrect

## Examples

### Retrieving a Ticket
User: "Look up FreeScout ticket 42"

1. Run: `python3 scripts/fetch_ticket.py 42`
2. Parse the JSON response
3. Display formatted conversation with all threads in chronological order

### Pushing a Draft Reply (with ticket ID)
User: "Push a draft reply to ticket #123"

1. Fetch ticket #123 if not in context
2. Review session context
3. Generate styled reply
4. Show plain text preview to user
5. Ask: "Does this look good to push as a draft?"
6. Once approved, convert to HTML and push
7. Confirm with review link

### Pushing a Draft Reply (without ticket ID)
User: "Draft a reply to the customer"

1. Scan conversation context for previously retrieved ticket ID
2. If found, proceed with that ticket
3. If not found, ask: "Which ticket would you like me to draft a reply for?"
4. Follow steps 3-7 above
