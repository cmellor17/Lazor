import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import LazorParser
from board import SetUpBoard
from blocks import Add

class TestBlockProperties(unittest.TestCase):
    def setUp(self):
        
        parser = LazorParser('data/mad_1.bff')
        data = parser.parse()
        board = SetUpBoard(data['grid'],
                           [pos for pos, _ in data['lazors']],
                           [dir for _, dir in data['lazors']],
                           data['block_counts'])
        sample_space = board.sampler(data['grid'])
        sampled_grid = board.sample_board(sample_space, data['block_counts'], data['grid'])
        self.meshgrid = board.make_board(sampled_grid)

    def test_reflect_block(self):
        # Loop through and find the first 'A' in meshgrid
        for y, row in enumerate(self.meshgrid):
            for x, cell in enumerate(row):
                if cell == 'A':
                    block = Add(x, y)
                    reflect, transmit = block.prop(self.meshgrid)
                    self.assertTrue(reflect)
                    self.assertFalse(transmit)
                    return  
                
    def test_transmit_only_or_empty(self):
        # Find a cell that's 'o'
        for y, row in enumerate(self.meshgrid):
            for x, cell in enumerate(row):
                if cell == 'o':
                    block = Add(x, y)
                    reflect, transmit = block.prop(self.meshgrid)
                    self.assertFalse(reflect)
                    self.assertTrue(transmit)
                    return

if __name__ == '__main__':
    unittest.main()
