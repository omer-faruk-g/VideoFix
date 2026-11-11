"""VideoFix read-only check: what is already in place, what is a gap.

Usage: python check.py [--project DIR] [--home DIR]
Changes nothing. Exit code 0 always (it is a report, not a gate).
"""
import argparse
import json
import os
from pathlib import Path


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def mcp_servers(home, project):
    """Map server name -> config from user (~/.claude.json, top level and this
    project's entry) and project (.mcp.json) scopes."""
    servers = {}
    user = load_json(home / ".claude.json")
    servers.update(user.get("mcpServers") or {})
    for key, entry in (user.get("projects") or {}).items():
        if Path(key).resolve() == project.resolve():
            servers.update((entry or {}).get("mcpServers") or {})
    servers.update(load_json(project / ".mcp.json").get("mcpServers") or {})
    return servers


def enabled_plugins(home, project):
    names = []
    for f in (home / ".claude" / "settings.json", project / ".claude" / "settings.json"):
        for name, on in (load_json(f).get("enabledPlugins") or {}).items():
            if on:
                names.append(name.lower())
    return names


def has_tool(word, servers, plugins):
    return any(word in n.lower() for n in servers) or any(word in p for p in plugins)


def is_read_only(cfg):
    blob = json.dumps(cfg).lower()
    return "--read-only" in blob or "read_only=true" in blob


def run(project, home):
    out = []
    skills = home / ".claude" / "skills"
    servers = mcp_servers(home, project)
    plugins = enabled_plugins(home, project)

    def add(status, video, msg):
        out.append(f"[{status}] {video}: {msg}")

    # Video 1: code graph
    if not (skills / "graphify").is_dir():
        add("GAP", "v1 graph", "graphify skill not installed; use Grep -n + ranged Read (install only on user's yes)")
    elif (project / "graphify-out").is_dir():
        add("OK", "v1 graph", "graphify-out/ exists; query it before broad reads")
    else:
        add("INFO", "v1 graph", "graphify installed, no graph for this project; worth it only for large/unfamiliar code")

    # Videos 3, 5: session hygiene
    settings_txt = json.dumps(load_json(home / ".claude" / "settings.json"))
    if (skills / "claudelimit").is_dir() and "ctx_hook.py" in settings_txt:
        add("OK", "v3/v5 limits", "claudelimit installed with context hooks")
    elif (skills / "claudelimit").is_dir():
        add("GAP", "v3/v5 limits", "claudelimit installed but its context hook is not in settings.json")
    else:
        add("GAP", "v3/v5 limits", "no claudelimit; follow VideoFix section 1 by hand")

    claude_md = project / "CLAUDE.md"
    if claude_md.is_file():
        n = len(claude_md.read_text(encoding="utf-8", errors="replace").splitlines())
        add("OK" if n < 200 else "GAP", "v3 memory", f"CLAUDE.md {n} lines" + ("" if n < 200 else " (keep under 200)"))
    else:
        add("INFO", "v3 memory", "no project CLAUDE.md; put repeated instructions there once")

    # Video 2: API keys
    env = project / ".env"
    if env.is_file():
        gi = project / ".gitignore"
        ignored = gi.is_file() and any(
            line.strip() in (".env", "/.env", ".env*", "*.env")
            for line in gi.read_text(encoding="utf-8", errors="replace").splitlines()
        )
        add("OK" if ignored else "GAP", "v2 api keys", ".env is git-ignored" if ignored else ".env exists but is not in .gitignore")
    else:
        add("INFO", "v2 api keys", "no .env; read API keys from environment when you add one")

    # Video 4: ship gate tools
    if has_tool("playwright", servers, plugins):
        add("OK", "v4 browser", "Playwright available")
    else:
        add("INFO", "v4 browser", "no Playwright MCP; use the desktop app's built-in browser for the visual check")
    add("OK" if (skills / "security-review").is_dir() else "GAP", "v4 security",
        "security-review skill present" if (skills / "security-review").is_dir() else "no security-review skill; use VideoFix section 3.2 list")
    if has_tool("context7", servers, plugins):
        add("OK", "v4 docs", "Context7 available")
    else:
        add("INFO", "v4 docs", "no Context7; check lockfile version + official docs before using an API")
    for name, cfg in servers.items():
        if "supabase" in name.lower() or "postgres" in name.lower():
            add("OK" if is_read_only(cfg) else "GAP", "v4 database",
                f"MCP '{name}' " + ("is read-only" if is_read_only(cfg) else "can write; use --read-only / a dev branch first"))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--project", default=os.getcwd())
    ap.add_argument("--home", default=str(Path.home()))
    a = ap.parse_args()
    for line in run(Path(a.project), Path(a.home)):
        print(line)


if __name__ == "__main__":
    main()
