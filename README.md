# Claude Work Journal

A template repo for keeping a weekly work journal with [Claude Code](https://claude.com/claude-code). It collects what you actually did each week and turns it into a Markdown journal you can reuse later, whether you work at a product company, as a consultant, or on side projects in the evenings.

You say *"write the journal for this week"*, and Claude:

1. Reads your **Claude Code prompt history** for the week. This is usually the best record of what you worked on.
2. Collects your **git commits** across your repos.
3. Optionally pulls from **any issue tracker, wiki or calendar** you have a connector or CLI for: GitHub, Jira, Linear, Confluence, Notion, Google Calendar…
4. Writes `weeks/2026/2026-W10.md` from the template, then commits it.

See [`examples/2026-W10.md`](examples/2026-W10.md) for a sample result (fictional).

## Why

Six months later, nobody remembers what they did in week 10. Writing it down by hand doesn't happen. Your prompt history and commits already hold the record; this turns them into prose once a week, while you still remember enough to correct it.

What people use it for:

- **Performance reviews and promotion cases**: a year of concrete, dated work instead of a blank page.
- **Consulting**: assignment reports and CV updates per client.
- **Side projects**: a devlog of what you built and what you learned, without extra effort.
- **Standups and retros**: "what did I actually do last week?"

The skill is deliberately conservative:

- It only claims what the sources show. Work that was only investigated isn't reported as delivered, and work isn't moved between weeks.
- It doesn't name individual people. It uses roles instead ("the tester").
- It leaves out whatever you list under `exclude`, and tells you what it left out.
- It never invents hours.

## Getting started

1. Click **Use this template** on GitHub and create your repo. If the journal will mention employers or clients, make it **private**.
2. Clone it and edit `journal.config.yml`:
   - your projects and their repos (product, client, hobby... anything)
   - anything to keep out of the journal (`exclude`)
   - journal and reply language
   - extra `sources`: enable the examples or add your own. Each one is a single line in plain language saying what to fetch, and Claude uses whatever connector or CLI you have for it
3. Open Claude Code in the repo and ask:
   ```
   write the journal for this week
   ```
   or `fill in week 9`, or in any other language.

Requirements: Claude Code and `python3` (3.8+, standard library only). Extra sources need their connector or CLI (e.g. `gh` for GitHub); without them, prompt history and git work on their own.

## Layout

```
.claude/skills/weekly-journal/   the skill and the history script
journal.config.yml               your sources, projects and languages
templates/weekly-template.md     sections of a week file
weeks/YYYY/YYYY-WNN.md           your journal
highlights/                      achievements and technologies, distilled across weeks
examples/                        a fictional week for reference
```

## Customising

- **Template**: change the sections in `templates/weekly-template.md`. The skill follows whatever headings it finds there.
- **Sources**: add an entry under `sources` in `journal.config.yml`. If a source needs more detailed handling, add a note under "Known sources" in `.claude/skills/weekly-journal/SKILL.md`.
- **Rules**: everything else in `SKILL.md` is plain instructions you can edit.

## Privacy

`scripts/claude_history.py` reads `~/.claude/history.jsonl` locally and only prints prompts from the requested week. Nothing is sent anywhere except through your Claude Code session. Your journal stays in your own repo.

## License

MIT
