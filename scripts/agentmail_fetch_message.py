#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

OPENCLAW_CONFIG = Path('/home/var/.openclaw/openclaw.json')


def load_key() -> str:
    cfg = json.loads(OPENCLAW_CONFIG.read_text())
    key = cfg.get('env', {}).get('AGENTMAIL_API_KEY')
    if not key:
        raise SystemExit('AGENTMAIL_API_KEY missing from /home/var/.openclaw/openclaw.json')
    return key


def request(path: str) -> dict:
    key = load_key()
    req = urllib.request.Request(
        'https://api.agentmail.to/v0' + path,
        headers={'Authorization': f'Bearer {key}', 'Accept': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode('utf-8', 'replace'))


def emit_message(inbox: str, full: dict, subject_fallback: str = '') -> int:
    text = full.get('text') or full.get('extracted_text') or full.get('preview') or ''
    out = {
        'inbox_id': full.get('inbox_id') or inbox,
        'message_id': full.get('message_id') or full.get('id'),
        'thread_id': full.get('thread_id'),
        'subject': full.get('subject') or subject_fallback,
        'from': full.get('from'),
        'to': full.get('to'),
        'timestamp': full.get('timestamp'),
        'text': text,
        'headers': full.get('headers', {}),
    }
    print(json.dumps(out, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--inbox', required=True)
    ap.add_argument('--subject')
    ap.add_argument('--message-id')
    args = ap.parse_args()

    if not args.subject and not args.message_id:
        raise SystemExit('Provide either --subject or --message-id')

    inbox_q = urllib.parse.quote(args.inbox, safe='')

    if args.message_id:
        mid = urllib.parse.quote(args.message_id, safe='')
        full = request(f'/inboxes/{inbox_q}/messages/{mid}')
        return emit_message(args.inbox, full, subject_fallback=args.subject or '')

    listing = request(f'/inboxes/{inbox_q}/messages?limit=100')
    for msg in listing.get('messages', []):
        if (msg.get('subject') or '') == args.subject:
            mid = urllib.parse.quote(msg.get('message_id') or msg.get('id') or '', safe='')
            full = request(f'/inboxes/{inbox_q}/messages/{mid}')
            return emit_message(args.inbox, full, subject_fallback=args.subject or '')
    raise SystemExit(f'No message found in {args.inbox} with subject: {args.subject}')


if __name__ == '__main__':
    raise SystemExit(main())
