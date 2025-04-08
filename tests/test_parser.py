import unittest
from parser import LazorParser
import os

class TestLazorParser(unittest.TestCase):
    def test_parse_mad_1(self):
        lazor_path = os.path.join('data', 'mad_1.bff')  # adjust if needed
        parser = LazorParser(lazor_path)
        result = parser.parse()

        # Sanity checks - update these based on your actual mad_1.bff
        self.assertIn('grid', result)
        self.assertIn('block_counts', result)
        self.assertIn('lazors', result)
        self.assertIn('points', result)

        print("Parsed result:", result)

if __name__ == '__main__':
    unittest.main()