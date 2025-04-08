import random
import copy

class SetUpBoard:
    ...

    def __init__(self, grid, origin, path, sets):
        self.grid = grid
        self.origin = origin
        self.path = path
        self.sets = sets

    def sample_board(self, sample_space, blocks, grid=None):
        """
        Randomly places blocks on allowed positions of the board.

        Parameters:
            sample_space (list[tuple[int, int]]): Coordinates for block placement
            blocks (dict): Dictionary with block types ('A', 'B', 'C') and counts
            grid (list[list[str]]): Initial board layout (optional)

        Returns:
            grid (list[list[str]]): Grid with blocks placed
        """
        grid = copy.deepcopy(grid or self.grid)
        total_blocks = sum(blocks.values())
        options = random.sample(sample_space, total_blocks)

        nA = blocks.get('A', 0)
        nB = blocks.get('B', 0)
        nC = blocks.get('C', 0)

        blocks = {'A': nA, 'B': nB, 'C': nC}
        block_pool = ['A'] * nA + ['B'] * nB + ['C'] * nC
        random.shuffle(block_pool)
        
        for (i, j), block_type in zip(options, block_pool):
            grid[j][i] = block_type
        
        return grid
