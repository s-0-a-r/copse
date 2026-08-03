import os
import subprocess
import unittest

COPSE_BIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "copse"))
COPSE_TREE_BIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "copse-tree"))


class TestCopseCLI(unittest.TestCase):
    def test_copse_help_contains_all_subcommands(self):
        res = subprocess.run([COPSE_BIN, "--help"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        output = res.stdout
        self.assertIn("copse worktree", output)
        self.assertIn("copse fan", output)
        self.assertIn("copse ls", output)
        self.assertIn("copse diff", output)
        self.assertIn("copse clean", output)
        self.assertIn("copse watch", output)

    def test_copse_tree_help(self):
        res = subprocess.run([COPSE_TREE_BIN, "--help"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        output = res.stdout
        self.assertIn("--no-hidden", output)
        self.assertIn("-a, --all", output)

    def test_copse_ls_execution(self):
        res = subprocess.run([COPSE_BIN, "ls", "--project", os.getcwd()], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("SLOT", res.stdout)
        self.assertIn("BRANCH", res.stdout)
        self.assertIn("STATUS", res.stdout)
        self.assertIn("PATH", res.stdout)

    def test_copse_ls_fan_only(self):
        res = subprocess.run([COPSE_BIN, "ls", "--fan-only", "--project", os.getcwd()], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("SLOT", res.stdout)

    def test_copse_clean_dry_run(self):
        res = subprocess.run([COPSE_BIN, "clean", "--dry-run", "--project", os.getcwd()], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

    def test_copse_diff_too_many_args(self):
        res = subprocess.run([COPSE_BIN, "diff", "1", "2", "3", "--project", os.getcwd()], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Error: copse diff accepts at most 2 slot arguments", res.stderr)

    def test_copse_diff_slot_not_found(self):
        res = subprocess.run([COPSE_BIN, "diff", "999", "--project", os.getcwd()], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Slot 999 not found", res.stderr)

    def test_copse_diff_two_slots_not_found(self):
        res = subprocess.run([COPSE_BIN, "diff", "1", "999", "--project", os.getcwd()], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Slot 999 not found", res.stderr)

    def test_copse_clean_no_worktrees(self):
        res = subprocess.run([COPSE_BIN, "clean", "--project", os.getcwd()], input="", capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

    def test_copse_watch_no_active_slots(self):
        res = subprocess.run([COPSE_BIN, "watch", "--project", os.getcwd()], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("No active fan slots with agent panes found to watch.", res.stdout)

    def test_copse_worktree_missing_branch(self):
        res = subprocess.run([COPSE_BIN, "worktree"], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Usage: copse worktree", res.stderr)

    def test_copse_fan_missing_task(self):
        res = subprocess.run([COPSE_BIN, "fan"], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Usage: copse fan", res.stderr)


if __name__ == "__main__":
    unittest.main()


