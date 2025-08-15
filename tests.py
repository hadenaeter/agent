from functions.write_file import write_file
from functions.get_file_content import get_file_content
import unittest

class TestGetFileContent(unittest.TestCase):
    def test_write_file(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        with open("calculator/lorem.txt", "r") as f:
            contents = f.read()
        self.assertEqual("wait, this isn't lorem ipsum", contents)

    def test_write_new_file(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)
        with open("calculator/pkg/morelorem.txt", "r") as f:
            contents = f.read()
            self.assertEqual("lorem ipsum dolor sit amet", contents)

    def test_write_outside_boundary(self):
        error = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(error)
        self.assertEqual(error,
            "Result for '/tmp/temp.txt' file:\n    Error: Cannot write to " + '"/tmp/temp.txt" as it is outside the permitted working directory')

if __name__ == "__main__":
    unittest.main()
