import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check  # noqa: E402


def lines_for(result, key):
    return [l for l in result if key in l]


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.home = root / "home"
        self.proj = root / "proj"
        (self.home / ".claude" / "skills").mkdir(parents=True)
        self.proj.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self):
        return check.run(self.proj, self.home)

    def test_empty_setup_reports_gaps_and_infos(self):
        r = self.run_check()
        self.assertTrue(lines_for(r, "v1 graph")[0].startswith("[GAP]"))
        self.assertTrue(lines_for(r, "v3/v5 limits")[0].startswith("[GAP]"))
        self.assertTrue(lines_for(r, "v4 browser")[0].startswith("[INFO]"))
        self.assertFalse(lines_for(r, "v4 database"))

    def test_graph_present(self):
        (self.home / ".claude" / "skills" / "graphify").mkdir()
        (self.proj / "graphify-out").mkdir()
        self.assertTrue(lines_for(self.run_check(), "v1 graph")[0].startswith("[OK]"))

    def test_env_not_ignored_is_gap_then_ok(self):
        (self.proj / ".env").write_text("KEY=x\n")
        self.assertTrue(lines_for(self.run_check(), "v2 api keys")[0].startswith("[GAP]"))
        (self.proj / ".gitignore").write_text("node_modules\n.env\n")
        self.assertTrue(lines_for(self.run_check(), "v2 api keys")[0].startswith("[OK]"))

    def test_long_claude_md_is_gap(self):
        (self.proj / "CLAUDE.md").write_text("x\n" * 250)
        self.assertIn("250 lines", lines_for(self.run_check(), "v3 memory")[0])
        self.assertTrue(lines_for(self.run_check(), "v3 memory")[0].startswith("[GAP]"))

    def test_supabase_write_vs_read_only(self):
        mcp = {"mcpServers": {"supabase": {"command": "npx", "args": ["-y", "@supabase/mcp-server-supabase"]}}}
        (self.proj / ".mcp.json").write_text(json.dumps(mcp))
        self.assertTrue(lines_for(self.run_check(), "v4 database")[0].startswith("[GAP]"))
        mcp["mcpServers"]["supabase"]["args"].append("--read-only")
        (self.proj / ".mcp.json").write_text(json.dumps(mcp))
        self.assertTrue(lines_for(self.run_check(), "v4 database")[0].startswith("[OK]"))

    def test_user_scope_tools_and_claudelimit_hook(self):
        (self.home / ".claude.json").write_text(json.dumps({"mcpServers": {"context7": {}, "playwright": {}}}))
        (self.home / ".claude" / "skills" / "claudelimit").mkdir()
        (self.home / ".claude" / "settings.json").write_text(
            json.dumps({"hooks": {"UserPromptSubmit": [{"hooks": [{"command": "python ctx_hook.py prompt"}]}]}}))
        r = self.run_check()
        self.assertTrue(lines_for(r, "v4 docs")[0].startswith("[OK]"))
        self.assertTrue(lines_for(r, "v4 browser")[0].startswith("[OK]"))
        self.assertTrue(lines_for(r, "v3/v5 limits")[0].startswith("[OK]"))

    def test_bad_json_does_not_crash(self):
        (self.proj / ".mcp.json").write_text("{not json")
        self.assertTrue(self.run_check())


if __name__ == "__main__":
    unittest.main()
