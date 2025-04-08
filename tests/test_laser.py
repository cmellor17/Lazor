import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import LazorParser
from board import SetUpBoard
from laser import Laser

class TestLaserTrajectory(unittest.TestCase):
    def setUp(self):
        parser = LazorParser('data/mad_1.bff')
        data = parser.parse()

        self.grid = data['grid']
        self.origin = [p for p, _ in data['lazors']]
        self.path = [d for _, d in data['lazors']]
        self.blocks = data['block_counts']
        self.targets = data['points']

        self.board = SetUpBoard(self.grid, self.origin, self.path, self.blocks)
        sample_space = self.board.sampler(self.grid)
        sampled_grid = self.board.sample_board(sample_space, self.blocks, self.grid)
        self.meshgrid = self.board.make_board(sampled_grid)

    def test_laser_hits_grid(self):
        laser = Laser(self.origin, self.path)
        intercepts, paths, refracted = laser.trajectory(self.path, self.grid, self.meshgrid)

        self.assertIsInstance(intercepts, list)
        self.assertGreater(len(intercepts), 0)
        self.assertTrue(all(isinstance(p, tuple) for p in intercepts))

    def test_laser_inside_bounds(self):
        laser = Laser(self.origin, self.path)
        intercepts, _, _ = laser.trajectory(self.path, self.grid, self.meshgrid)

        max_x = len(self.meshgrid[0])
        max_y = len(self.meshgrid)

        for x, y in intercepts:
            self.assertTrue(0 <= x < max_x)
            self.assertTrue(0 <= y < max_y)

if __name__ == '__main__':
    unittest.main()
