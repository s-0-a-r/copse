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

    def test_scan_dir_default_hides_dotfiles(self):
        nodes = scan_dir(self.root, 0, show_hidden=False)
        names = [n["name"] for n in nodes]
        self.assertIn("normal_dir", names)
        self.assertIn("normal_file.txt", names)
        self.assertNotIn(".hidden_dir", names)
        self.assertNotIn(".hidden_file", names)

    def test_scan_dir_show_hidden(self):
        nodes = scan_dir(self.root, 0, show_hidden=True)
        names = [n["name"] for n in nodes]
        self.assertIn("normal_dir", names)
        self.assertIn("normal_file.txt", names)
        self.assertIn(".hidden_dir", names)
        self.assertIn(".hidden_file", names)

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

        # Toggle back
        tree.toggle_hidden()
        self.assertFalse(tree.show_hidden)
        names_back = [n["name"] for n in tree.nodes]
        self.assertNotIn(".hidden_file", names_back)
        self.assertNotIn(".hidden_dir", names_back)
        self.assertIn("file_inside.txt", names_back)


if __name__ == "__main__":
    unittest.main()
