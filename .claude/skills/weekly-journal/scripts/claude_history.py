#!/usr/bin/env python3
"""Print Claude Code prompts from ~/.claude/history.jsonl for one ISO week.

Usage: claude_history.py <iso-year> <iso-week> [--width N] [--history PATH]

Skips slash commands and very short prompts ("ok", "yes", "2" ...).
Output: one line per prompt, "<weekday> <MM-DD HH:MM> <project> | <prompt>".
"""
import argparse
import datetime
import json
import os

parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
parser.add_argument("year", type=int)
parser.add_argument("week", type=int)
parser.add_argument("--width", type=int, default=150, help="max characters per prompt")
parser.add_argument("--history", default="~/.claude/history.jsonl")
args = parser.parse_args()

start = datetime.datetime.fromisocalendar(args.year, args.week, 1)
end = start + datetime.timedelta(days=7)
s, e = start.timestamp() * 1000, end.timestamp() * 1000

print(f"# Week {args.year}-W{args.week:02d}: {start:%Y-%m-%d} .. {(end - datetime.timedelta(days=1)):%Y-%m-%d}")
with open(os.path.expanduser(args.history), encoding="utf-8") as f:
    for line in f:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        t = d.get("timestamp", 0)
        if not (s <= t < e):
            continue
        text = d.get("display", "").replace("\n", " ").strip()
        if text.startswith("/") or len(text) < 4:
            continue
        when = datetime.datetime.fromtimestamp(t / 1000).strftime("%a %m-%d %H:%M")
        project = d.get("project", "").rstrip("/").split("/")[-1]
        print(f"{when} {project} | {text[:args.width]}")
