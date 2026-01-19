#!/usr/bin/env python3
"""
Push a draft reply to a FreeScout ticket.

Usage:
  python push_draft.py <ticket_id> <message>
  python push_draft.py <ticket_id> --stdin  (reads message from stdin)

Requires ~/.freescout/config.json with:
{
  "url": "support.example.com",
  "api_key": "your-api-key",
  "mailbox_id": 1,
  "user_id": 1  // Your FreeScout user ID (required for posting replies)
}
"""

import json
import sys
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def load_config():
    """Load FreeScout configuration from ~/.freescout/config.json"""
    config_path = os.path.expanduser("~/.freescout/config.json")

    if not os.path.exists(config_path):
        return None, f"Config file not found at {config_path}"

    with open(config_path, 'r') as f:
        config = json.load(f)

    required = ['url', 'api_key', 'user_id']
    missing = [k for k in required if k not in config]
    if missing:
        return None, f"Missing config keys: {', '.join(missing)}. Note: user_id is required for posting replies."

    return config, None


def push_draft(config, ticket_id, message):
    """Push a draft reply to a FreeScout ticket."""
    ticket_id = str(ticket_id).lstrip('#')

    base_url = config['url'].rstrip('/')
    if not base_url.startswith('http'):
        base_url = f"https://{base_url}"

    url = f"{base_url}/api/conversations/{ticket_id}/threads"

    payload = {
        "type": "message",
        "text": message,
        "user": config['user_id'],
        "state": "draft"
    }

    data = json.dumps(payload).encode('utf-8')

    req = Request(url, data=data, method='POST')
    req.add_header('X-FreeScout-API-Key', config['api_key'])
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')

    try:
        with urlopen(req) as response:
            thread_id = response.headers.get('Resource-ID', 'unknown')
            return {
                "success": True,
                "ticket_id": ticket_id,
                "thread_id": thread_id,
                "message": "Draft reply created successfully",
                "url": f"{base_url}/conversation/{ticket_id}"
            }
    except HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ""
        return {
            "success": False,
            "error": f"API error: {e.code} {e.reason}",
            "details": error_body
        }
    except URLError as e:
        return {
            "success": False,
            "error": f"Connection error: {e.reason}"
        }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: push_draft.py <ticket_id> <message> OR push_draft.py <ticket_id> --stdin"
        }))
        sys.exit(1)

    ticket_id = sys.argv[1]

    # Get message from stdin or argument
    if len(sys.argv) >= 3:
        if sys.argv[2] == '--stdin':
            message = sys.stdin.read().strip()
        else:
            message = ' '.join(sys.argv[2:])
    else:
        print(json.dumps({
            "success": False,
            "error": "No message provided. Use: push_draft.py <ticket_id> <message> OR push_draft.py <ticket_id> --stdin"
        }))
        sys.exit(1)

    if not message:
        print(json.dumps({
            "success": False,
            "error": "Empty message provided"
        }))
        sys.exit(1)

    config, error = load_config()
    if error:
        print(json.dumps({
            "success": False,
            "error": error
        }))
        sys.exit(1)

    result = push_draft(config, ticket_id, message)
    print(json.dumps(result, indent=2))

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
