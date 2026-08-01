import importlib.machinery
import importlib.util
import os
import sys
import tempfile
import unittest

# Import copse-tree from bin/
bin_path = os.path.join(os.path.dirname(__file__), "..", "bin", "copse-tree")
spec = importlib.util.spec_from_loader(
    "copse_tree", importlib.machinery.SourceFileLoader("copse_tree", bin_path)
)
copse_tree = importlib.util.module_from_spec(spec)
spec.loader.exec_module(copse_tree)

scan_dir = copse_tree.scan_dir
FileTree = copse_tree.FileTree


class TestCopseTree(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.root = self.test_dir.name

        os.makedirs(os.path.join(self.root, "normal_dir"))
        os.makedirs(os.path.join(self.root, ".hidden_dir"))

        with open(os.path.join(self.root, "normal_file.txt"), "w") as f:
            f.write("hello")
        with open(os.path.join(self.root, ".hidden_file"), "w") as f:
            f.write("secret")
        with open(os.path.join(self.root, "normal_dir", "file_inside.txt"), "w") as f:
            f.write("inside")
        with open(os.path.join(self.root, ".hidden_dir", "hidden_inside.txt"), "w") as f:
            f.write("inside hidden")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_scan_dir_default_shows_dotfiles(self):
        nodes = scan_dir(self.root, 0)
        names = [n["name"] for n in nodes]
        self.assertIn("normal_dir", names)
        self.assertIn("normal_file.txt", names)
        self.assertIn(".hidden_dir", names)
        self.assertIn(".hidden_file", names)

    def test_scan_dir_hide_dotfiles(self):
        nodes = scan_dir(self.root, 0, show_hidden=False)
        names = [n["name"] for n in nodes]
        self.assertIn("normal_dir", names)
        self.assertIn("normal_file.txt", names)
        self.assertNotIn(".hidden_dir", names)
        self.assertNotIn(".hidden_file", names)

    def test_file_tree_default_shows_dotfiles(self):
        tree = FileTree(self.root)
        names = [n["name"] for n in tree.nodes]
        self.assertIn(".hidden_file", names)
        self.assertIn(".hidden_dir", names)


    def test_file_tree_toggle_hidden(self):
        tree = FileTree(self.root, show_hidden=False)
        names = [n["name"] for n in tree.nodes]
        self.assertNotIn(".hidden_file", names)

        # Expand normal_dir
        normal_dir_idx = next(i for i, n in enumerate(tree.nodes) if n["name"] == "normal_dir")
        tree.expand(normal_dir_idx)
        names_expanded = [n["name"] for n in tree.nodes]
        self.assertIn("file_inside.txt", names_expanded)

        # Toggle hidden
        tree.toggle_hidden()
        self.assertTrue(tree.show_hidden)
        names_after = [n["name"] for n in tree.nodes]
        self.assertIn(".hidden_file", names_after)
        self.assertIn(".hidden_dir", names_after)
        # Verify expanded state maintained
        self.assertIn("file_inside.txt", names_after)

        # Select a hidden file
        hidden_idx = next(i for i, n in enumerate(tree.nodes) if n["name"] == ".hidden_file")
        tree.cursor = hidden_idx

        # Toggle back to hidden
        tree.toggle_hidden()
        self.assertFalse(tree.show_hidden)
        names_back = [n["name"] for n in tree.nodes]
        self.assertNotIn(".hidden_file", names_back)
        self.assertNotIn(".hidden_dir", names_back)
        # Verify cursor is within valid range and didn't crash
        self.assertTrue(0 <= tree.cursor < len(tree.nodes))

    def test_file_tree_scroll_clamping(self):
        tree = FileTree(self.root, show_hidden=True)
        tree.scroll = 100
        class DummyStdScr:
            def getmaxyx(self):
                return (10, 80)
            def erase(self):
                pass
            def addstr(self, *args):
                pass
            def refresh(self):
                pass

        import unittest.mock
        with unittest.mock.patch('curses.color_pair', return_value=0):
            tree.draw(DummyStdScr())
        # Verify scroll is clamped to max_scroll (max(0, 4 - 9) = 0)
        self.assertEqual(tree.scroll, 0)

    def test_cli_argument_parsing(self):
        parser = copse_tree.create_parser()

        # Default
        args = parser.parse_args([])
        self.assertTrue(args.show_hidden)

        # --no-hidden
        args = parser.parse_args(["--no-hidden"])
        self.assertFalse(args.show_hidden)

        # --no-hidden -a
        args = parser.parse_args(["--no-hidden", "-a"])
        self.assertTrue(args.show_hidden)



if __name__ == "__main__":
    unittest.main()


