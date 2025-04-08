def flatten(nested_list):
    """
    Flattens a nested list of lists into a single list.
    """
    return [item for sublist in nested_list for item in sublist]

def print_grid(grid):
    """
    Nicely prints a 2D grid (coarse or mesh).
    """
    for row in grid:
        print(" ".join(row))

def is_inside(x, y, width, height):
    """
    Check if a coordinate is inside a grid of given dimensions.
    """
    return 0 <= x < width and 0 <= y < height

def compare_point_sets(set1, set2):
    """
    Compare two sets of points (tuples) to check if they match.
    """
    return set(set1).issubset(set(set2))

def format_output_grid(meshgrid):
    """
    Extracts the coarse board from a meshgrid by skipping even rows/cols.
    """
    return [[meshgrid[j][i] for i in range(1, len(meshgrid[0]), 2)] for j in range(1, len(meshgrid), 2)]
