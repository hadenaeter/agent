from functions.run_python import run_python_file
import unittest

class TestGetFileContent(unittest.TestCase):
    def test_run_python_file(self):
        result = run_python_file("calculator", "main.py")
        expected = "Calculator App"
        print(result)
        self.assertTrue(expected in result)

    def test_calculation(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        expected = "3 + 5"
        print(result)
        self.assertTrue(expected in result)

    def test_tests(self):
        result = run_python_file("calculator", "tests.py")
        expected = "tests in "
        print(result)
        self.assertTrue(expected in result)

    def test_parent_dir(self):
        result = run_python_file("calculator", "../main.py")
        expected = "Error: "
        print(result)
        self.assertTrue(expected in result)

    def test_non_existent_file(self):
        result = run_python_file("calculator", "nonexistent.py")
        expected = "Error:"
        print(result)
        self.assertTrue(expected in result)

if __name__ == "__main__":
    unittest.main()
