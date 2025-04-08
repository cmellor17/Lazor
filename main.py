import os
import unittest
from lazor_parser import LazorParser
from board import SetUpBoard
from laser import Laser
from utils import compare_point_sets, print_grid, format_output_grid
from solver import outputter

def run_lazor_solver(filename, maxiter=10000):
    """
    Main driver function to run the Lazor game solver.

    Parameters:
        filename (str): Path to the .bff file
        maxiter (int): Maximum number of attempts for block placements
    """
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return
    
    attempts = set() # Track attempted grids to avoid trying the same ones over and over
    
    for i in range(maxiter):
        laz_parser = LazorParser(filename)
        data = laz_parser.parse()

        board = SetUpBoard(
            grid=data['grid'],
            origin=[pos for pos, _ in data['lazors']],
            path=[dir for _, dir in data['lazors']],
            sets=data['block_counts']
        )

        # Define sampler and make_board here if not part of the class
        def sampler(grid):
            return [(i, j) for j, row in enumerate(grid) for i, val in enumerate(row) if val == 'o']

        def make_board(grid):
            mesh_height = 2 * len(grid) + 1
            mesh_width = 2 * len(grid[0]) + 1
            meshgrid = [['o' for _ in range(mesh_width)] for _ in range(mesh_height)]
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    meshgrid[2 * i + 1][2 * j + 1] = grid[i][j]
            return meshgrid

        sample_space = sampler(board.grid)
        attempted = True
        attempt_count = 0
        while attempted and attempt_count < 500:
            sampled_grid = board.sample_board(sample_space, board.sets, board.grid)
            grid_key = tuple(tuple(row) for row in sampled_grid)

            if grid_key not in attempts:
                attempted = False
                attempts.add(grid_key)
            
            attempt_count += 1

        mesh = make_board(sampled_grid)

        laser = Laser(board.origin, board.path)
        intercepts, _, refract_paths = laser.trajectory(board.path, board.grid, mesh)
        all_hits = intercepts + refract_paths

        if compare_point_sets(data['points'], all_hits):
            print(f"\nSolution found in {i + 1} iterations!")
            print("Final mesh board:")
            print_grid(mesh)
            print("\nFinal block layout:")
            print_grid(format_output_grid(mesh))
            outputter(mesh)
            return

        if i % 1000 == 0:
            print(f"[Iteration {i}] Trying new layout...")


    print("\nMax iteration allowance reached: no solution found")
    print("Block counts:", board.sets)
    print("Targets:", data['points'])
    print("Lazors:", list(zip(board.origin, board.path)))


def get_user_filename():
    while True:
        fname = input("Enter the name of a .bff file to solve: ").strip()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, "data", fname)
        if fname.endswith(".bff") and os.path.isfile(full_path):
            return full_path
        print("Please enter a valid existing .bff filename.")


if __name__ == '__main__':
    #filename = get_user_filename()
    filename = "g:\My Drive\School\classes\Software Carpentry\Lazor Project\data\dark_1.bff"
    run_lazor_solver(filename, maxiter=5000)
