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

    def test_copse_watch_execution_no_fan_slots(self):
        res = subprocess.run([COPSE_BIN, "watch", "--project", os.getcwd()], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("No active fan slots", res.stdout)



if __name__ == "__main__":
    unittest.main()
