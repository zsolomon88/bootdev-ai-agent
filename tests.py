import unittest
from functions.get_files_info import get_files_info

'''
class TestCalculator(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main()
'''

result = get_files_info("calculator", ".")
print(result)

result = get_files_info("calculator", "pkg")
print(result)

result = get_files_info("calculator", "/bin")
print(result)

result = get_files_info("calculator", "../")
print(result)

