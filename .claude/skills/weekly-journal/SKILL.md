---
name: weekly-journal
description: Fill in the work journal for a given week (weeks/YYYY/YYYY-WNN.md) from Claude Code history, git logs and, if configured, Jira and Confluence meeting notes. Use when the user asks to write, fill in or update the journal for a week ("write the journal for week 41", "fill in this week's journal", "ta vecka 41").
---

# Weekly work journal

Write one journal file per ISO week from the sources below, following `templates/weekly-template.md`. Read `journal.config.yml` first; it decides which sources to use, the languages, the projects and what to exclude. If a recent `weeks/YYYY/*.md` exists, match its tone and level of detail; otherwise use `examples/` for reference.

## 1. Pin down the week

- Get the Monday–Sunday dates of the ISO week. `python3 -c "import datetime as d; print(d.date.fromisocalendar(Y, W, 1))"` gives the Monday on any platform.
- "This week" means the week of today's date. "Week N" means ISO week N of the current year.
- The file is `weeks/<year>/<year>-W<NN>.md`. If it already exists, read it and update it instead of overwriting it.

## 2. Gather sources (run independent calls in parallel)

**Claude Code history** (always): usually the richest source.
```
python3 .claude/skills/weekly-journal/scripts/claude_history.py <year> <week> > <scratchpad>/wNN.txt
```
The output can be 30KB+, so write it to a scratch file and read that instead of printing it.

**Git commits**: the repos listed under `projects[].repos`, plus repos under `git.scan_dirs` that show activity (from the history or from a commit in the week). Use full timestamps: a bare date in `--until` takes the current time of day and pulls in the next Monday's commits.
```
for r in <repos>; do
  echo "== $r"; git -C $r log --all --since="<mon>T00:00" --until="<sun>T23:59" --author="<author>" \
    --format='%ad %s' --date=format:'%a %m-%d %H:%M' | sort -u | cut -c1-120; done
```
`<author>` comes from `git.authors` (repeat `--author` for each), or from `git config user.email` / `user.name` when the list is empty.

**Jira** (only if `jira.enabled`; Atlassian MCP connector). Use `jira.cloud_id`, or look it up once with `getAccessibleAtlassianResources`.
```
(assignee = currentUser() OR reporter = currentUser() OR assignee was currentUser() DURING ("<mon>","<sun>"))
AND updated >= "<mon>" ORDER BY updated DESC
```
Request only `summary`, `status` and `created`. Ask for `description` only for issues you need to understand. Check `created` before claiming an issue was created during the week.

**Confluence meeting notes** (only if `confluence.enabled`): read each page in `confluence.meeting_note_pages` with `getConfluenceContent` (full detail, markdown). Take the meetings dated inside the week, including agenda, decisions and notes. Dates on running note pages can be wrong: cross-check with issues mentioned in an entry (for example an issue created after the stated date), put the meeting in the week the evidence points to, and tell the user.

**Time tracking**: never invent hours. If `time_tracking` names a tool you can't reach, say so in the report.

If a configured source isn't available (connector missing, repo moved), continue with the rest and say what was skipped.

## 3. Write the journal

- Write in `journal_language`, using the template's section headings.
- **Projects / Context**: list each project worked on that week, using the names in `projects` (work in repos not listed there gets a short descriptive name). The role is `default_role`, adjusted when the sources clearly show something else (for example DevOps for pipeline or infrastructure work).
- **Tasks**: group by project or theme, with bold lead-ins and issue keys. Include meetings with agenda and decisions.
- **Only claim what the sources show.** If a deploy failed, say so. If something was only investigated, don't call it delivered. Don't move work from one week into another.
- **Leave out anything matching `exclude`.** Mention in the reply what was left out, so the user can ask for it.
- **Don't name individual people.** Use roles such as "the tester", "a colleague" or "the product owner".
- **Next Steps**: only follow-ups that are actually open at the end of that week.
- When a week produces something worth keeping, suggest an addition to `highlights/achievements.md` or `highlights/technologies.md` in the reply. Don't edit those files unless the user agrees.

## 4. Report and commit

- Report briefly in `reply_language`: the sources used, the main content, and anything to check (days without activity, uncertain dates, left-out items, unreachable sources).
- If `auto_commit` is true, commit as soon as the journal is written, without asking:
  ```
  git add weeks/<year>/<year>-W<NN>.md && git commit -m "Week <year>-<NN>"
  ```
  If other week files changed in the same round, name them in the message. Include the commit hash in the report.
- Don't push unless asked.
