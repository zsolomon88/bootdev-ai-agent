import unittest
from functions.run_python_file import run_python_file
'''
class TestCalculator(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main()
'''

result = run_python_file("calculator", "main.py")

print(result)
result = run_python_file("calculator", "tests.py")
print(result)
result = run_python_file("calculator", "../main.py")
print(result)
result = run_python_file("calculator", "nonexistent.py")
print(result)