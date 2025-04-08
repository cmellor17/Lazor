import unittest
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blocks import Add

class TestBlockProperties(unittest.TestCase):
    def setUp(self):
        # Create a simple 5x5 meshgrid with each block type
        self.meshgrid = [['o' for _ in range(5)] for _ in range(5)]
        self.meshgrid[1][1] = 'A'  # Reflect
        self.meshgrid[2][2] = 'B'  # Opaque
        self.meshgrid[3][3] = 'C'  # Refract
        self.meshgrid[4][4] = 'o'  # Empty

    def test_reflect_block(self):
        block = Add(1, 1)
        reflect, transmit = block.prop(self.meshgrid)
        self.assertTrue(reflect)
        self.assertFalse(transmit)

    def test_opaque_block(self):
        block = Add(2, 2)
        reflect, transmit = block.prop(self.meshgrid)
        self.assertFalse(reflect)
        self.assertFalse(transmit)

    def test_refract_block(self):
        block = Add(3, 3)
        reflect, transmit = block.prop(self.meshgrid)
        self.assertTrue(reflect)
        self.assertTrue(transmit)

    def test_empty_cell(self):
        block = Add(4, 4)
        reflect, transmit = block.prop(self.meshgrid)
        self.assertFalse(reflect)
        self.assertTrue(transmit)

if __name__ == '__main__':
    unittest.main()
