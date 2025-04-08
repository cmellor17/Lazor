import unittest
from lazor_parser import LazorParser
from board import SetUpBoard
from laser import Laser
from utils import compare_point_sets, print_grid

def outputter(mesh):
    print("Analyzing and preparing files for output...")
    solution = []

    for j in range(1, len(mesh), 2):
        for i in range(1, len(mesh[0]), 2):
            solution.append(mesh[j][i])

    width = int((len(mesh[0]) - 1) * 0.5)
    solution = [solution[x:x + width] for x in range(0, len(solution), width)]

    with open('solution.bff', 'w') as file:
        for row in solution:
            file.write('\t'.join(row) + '\n')

    print("Solution found! Written to solution.bff")

def solution_generator(filename, maxiter=10):
    for i in range(maxiter):
        parser = LazorParser(filename)
        data = parser.parse()

        B = SetUpBoard(data['grid'], [pos for pos, _ in data['lazors']],
                       [dir for _, dir in data['lazors']], data['block_counts'])

        sample_space = B.sampler(B.grid)
        sampled_grid = B.sample_board(sample_space, B.sets, B.grid)
        mesh = B.make_board(sampled_grid)

        L = Laser(B.origin, B.path)
        intcp, _, intercept_new = L.trajectory(B.path, B.grid, mesh)
        total_intcp = intcp + intercept_new

        if compare_point_sets(total_intcp, data['points']):
            print(f"Solution found in {i + 1} iterations!")
            print_grid(mesh)
            outputter(mesh)
            return

        if i % 1000 == 0:
            print(f"[Iteration {i}] Trying new layout...")

    print("Max iteration allowance reached: no solution found")

def get_user_filename():
    while True:
        filename = input("Enter the filename (including extension): ").strip()
        if filename:
            return filename
        print("Invalid filename. Try again.")

if __name__ == '__main__':
    fname = get_user_filename()
    solution_generator(fname, 500000)
    