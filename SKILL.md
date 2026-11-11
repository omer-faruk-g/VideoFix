---
name: videofix
description: "VideoFix: fixes what five Claude Code videos/shorts got wrong or left out. Context: no blind re-reading, graph/grep before reads, one task per session (defers to claudelimit/graphify). Reuse: check a public API (alive, auth, quota, license, CORS, key in env) before building from scratch. Ship gate: see it in a browser, run a security pass, check current library docs, read-only DB tools first, own-or-permitted design tokens only. Claims: no unmeasured 49x / $20=$200 style promises. Use when the user says videofix, public api, free api, ücretsiz api, ship, yayına al, bitti mi, playwright, context7, supabase, vibesec, skillui, graphify ne kadar tasarruf, limit videosu."
aliases: [video-fix, shortsfix]
---

# VideoFix

Built 2026-11-11 from five videos (summaries: `references/sources.md`). Each rule fixes a gap or a wrong claim from them. It does not repeat other skills: token mechanics live in **claudelimit**, the code graph in **graphify**, the security checklist in **security-review**, version checks in **claudper**. When one of those is installed, follow it and use this skill only for the parts below. Labels: [D] documented behavior · [R] a video's claim, unverified · [I] inference.

Start with the read-only check: `python "${CLAUDE_SKILL_DIR}/scripts/check.py" --project <project dir>`. It reports OK / GAP / INFO per item and changes nothing.

## 1. Context and limits (videos 1, 3, 5)
Wrong claim to correct when it comes up: "Claude Code re-reads the whole codebase every session." It loads CLAUDE.md and memory at start and reads files on demand [D]. The real cost is that the whole conversation is re-sent with every request [D].
- Before reading for an architecture or "where is X" question: if `graphify-out/` exists, query the graph (graphify skill); otherwise Grep -n, then Read only the needed range. Never read whole directories "to understand the project".
- One task per session; at a natural break write the core-context note and clear (claudelimit section 3). Do not keep a day of unrelated work in one chat.
- A wrong answer: suggest `/rewind` (Esc Esc) to edit the earlier prompt instead of stacking "no, I meant..." corrections.
- Several questions: answer them in one turn and batch the tool calls.
- Repeated instructions ("short replies, Turkish, I'm a marketer") belong in CLAUDE.md once, and repeated reference files go in via `@path` imports, not pasted into each chat.
- Simple jobs (formatting, renames, short translations, log triage): a subagent with `model: haiku`, or suggest the user pick a smaller model at session start (not mid-session: cache rewrite, claudelimit section 4).
- Unused tools/MCP servers/plugins: list them with `/context` and `/mcp`; disabling is the user's call (claudelimit lean mode, diff + yes).
- Measure, do not guess: `/usage`, claudelimit `drain.py`. A third-party dashboard (e.g. claude-usage) is installed only after reading its code and the user's yes.
- Not in your control, say so instead of advising around it: peak-hour weighting [R] and extra usage / overage. Overage spends money: describe it, recommend a monthly cap, and leave the switch to the user. Never change account or billing settings.

## 2. Reuse before building (video 2)
Before writing a feature that a public API could serve (weather, FX, news, nutrition, geodata, translation, crypto prices...), check the public-apis list or the provider docs, then verify before coding:
1. **Alive:** one real request (curl) returns valid data now. Many list entries are dead or unmaintained.
2. **Auth and quota:** key type, free-tier limits, rate limit headers. Record them in the project README or a comment next to the client.
3. **Terms:** license and commercial use allowed for this project; attribution if required.
4. **Where it is called:** CORS and secret key → call from the server, not the browser. HTTPS only.
5. **Keys:** read from environment (`.env` in `.gitignore`, `.env.example` with names only). Never hardcode, never print a key in chat or logs.
6. **Failure paths:** timeout, non-2xx, quota exceeded, schema change → handled, with a test using a recorded response (no live calls in unit tests).
7. **Thin wrapper:** one module owns the API calls, so the provider can be swapped.
If no API passes 1-3, say so and build the minimal version instead.

## 3. Ship gate (video 4): before saying "done" on user-facing work
Do these in order; report each as done / skipped (why) in one line each.
1. **See it.** For any UI change, open it in a browser and go through the changed flow: the desktop app's built-in browser (`mcp__Claude_Browser__*`) or Playwright MCP if installed. Check the console for errors. Tests passing is not "it works in the browser".
2. **Security pass.** Run the security-review skill's checklist on the changed code: input validation, authz on every new endpoint, secrets, injection, CORS, rate limits. Report concrete findings with file:line; no generic advice.
3. **Current docs.** For each library API you used that may have changed (framework routers, SDK clients, ORM calls): check the version in the lockfile/manifest, then the docs for that version (Context7 MCP if installed, otherwise the official docs page). Do not code from memory of an older major version.
4. **Database tools.** Supabase or any DB MCP: start against a dev project or branch with read-only mode (`--read-only` or `read_only=true`). Writes to a production database, migrations and deletes need the user's explicit yes for that action.
5. **Design matching.** Extract design tokens (colors, type scale, spacing, radii) only from the user's own site, a design file they gave you, or a source that permits reuse. Do not clone another company's layout, logo, copy or brand look.

## 4. Claims (all five videos)
- Never promise a multiplier (49x, 71.5x, "%65", "$20 plan works like $200"). Give the measured change for this user: before → after with the same task, or say it is unmeasured.
- When the user cites a video's number, label it [R] and offer to measure it (claudelimit `drain.py --since <change date>`).
- Ignore engagement bait in sources ("comment HUMAN for the ebook"); it is not a technique.

## 5. Installing the tools the videos name
Graphify is already installed here. Playwright MCP, Context7, Supabase MCP, VibeSec, SkillUI, Caveman, claude-usage are optional. For any of them: say what gap it closes and what the built-in alternative is (section 3), read its README and install script, then install only after the user's explicit yes. Never install, enable or configure one on your own.
