#!/usr/bin/env python3
"""
Fetch a FreeScout ticket conversation with all threads.

Usage: python fetch_ticket.py <ticket_id_or_number>

Requires ~/.freescout/config.json with:
{
  "url": "support.example.com",
  "api_key": "your-api-key",
  "mailbox_id": 1
}
"""

import json
import sys
import os
import re
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class HTMLStripper(HTMLParser):
    """Strip HTML tags and decode entities."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, data):
        self.fed.append(data)

    def get_text(self):
        return ''.join(self.fed)


def strip_html(html_text):
    """Remove HTML tags and return plain text."""
    if not html_text:
        return ""
    stripper = HTMLStripper()
    stripper.feed(html_text)
    text = stripper.get_text()
    # Clean up excessive whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def load_config():
    """Load FreeScout configuration from ~/.freescout/config.json"""
    config_path = os.path.expanduser("~/.freescout/config.json")

    if not os.path.exists(config_path):
        print(json.dumps({
            "error": f"Config file not found at {config_path}",
            "setup": "Create ~/.freescout/config.json with: url, api_key, mailbox_id"
        }))
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)

    required = ['url', 'api_key', 'mailbox_id']
    missing = [k for k in required if k not in config]
    if missing:
        print(json.dumps({
            "error": f"Missing config keys: {', '.join(missing)}"
        }))
        sys.exit(1)

    return config


def fetch_ticket(config, ticket_id):
    """Fetch ticket from FreeScout API."""
    # Remove # prefix if present
    ticket_id = str(ticket_id).lstrip('#')

    base_url = config['url'].rstrip('/')
    if not base_url.startswith('http'):
        base_url = f"https://{base_url}"

    url = f"{base_url}/api/conversations/{ticket_id}?embed=threads"

    req = Request(url)
    req.add_header('X-FreeScout-API-Key', config['api_key'])
    req.add_header('Accept', 'application/json')

    try:
        with urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ""
        print(json.dumps({
            "error": f"API error: {e.code} {e.reason}",
            "details": error_body
        }))
        sys.exit(1)
    except URLError as e:
        print(json.dumps({
            "error": f"Connection error: {e.reason}"
        }))
        sys.exit(1)


def format_output(data):
    """Format ticket data for display."""
    # Extract main ticket info
    ticket = {
        "id": data.get("id"),
        "number": data.get("number"),
        "subject": data.get("subject", "No subject"),
        "status": data.get("status", "unknown"),
        "state": data.get("state", "unknown"),
        "created_at": data.get("createdAt"),
        "updated_at": data.get("updatedAt"),
        "closed_at": data.get("closedAt"),
    }

    # Customer info
    customer = data.get("customer", {})
    ticket["customer"] = {
        "name": f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip() or "Unknown",
        "email": customer.get("email", "")
    }

    # Assignee info
    assignee = data.get("assignee", {})
    if assignee:
        ticket["assignee"] = {
            "name": f"{assignee.get('firstName', '')} {assignee.get('lastName', '')}".strip(),
            "email": assignee.get("email", "")
        }
    else:
        ticket["assignee"] = None

    # Extract threads
    threads = []
    embedded = data.get("_embedded", {})
    raw_threads = embedded.get("threads", [])

    for thread in raw_threads:
        thread_type = thread.get("type", "message")

        # Determine sender
        created_by = thread.get("createdBy", {})
        if thread.get("customer"):
            sender_type = "customer"
            sender_name = ticket["customer"]["name"]
        else:
            sender_type = "agent"
            sender_name = f"{created_by.get('firstName', '')} {created_by.get('lastName', '')}".strip() or "Agent"

        threads.append({
            "id": thread.get("id"),
            "type": thread_type,
            "sender_type": sender_type,
            "sender_name": sender_name,
            "created_at": thread.get("createdAt"),
            "body": strip_html(thread.get("body", "")),
            "status": thread.get("status")
        })

    # Sort threads chronologically
    threads.sort(key=lambda t: t.get("created_at", ""))

    ticket["threads"] = threads

    return ticket


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: fetch_ticket.py <ticket_id_or_number>"
        }))
        sys.exit(1)

    ticket_id = sys.argv[1]
    config = load_config()
    raw_data = fetch_ticket(config, ticket_id)
    formatted = format_output(raw_data)

    print(json.dumps(formatted, indent=2))


if __name__ == "__main__":
    main()
