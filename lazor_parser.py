class LazorParser:
    def __init__(self, filename):
        self.filename = filename  # Save filename for later use

    def parse(self):
        with open(self.filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        grid = []
        block_counts = {}
        lazors = []
        points = []

        in_grid = False
        for line in lines:
            if line == "GRID START":
                in_grid = True
                continue
            if line == "GRID STOP":
                in_grid = False
                continue

            if in_grid:
                grid.append(list(line.replace(" ", "")))
            elif line and line[0] in ["A", "B", "C"] and len(line.split()) == 2:
                block_type, count = line.split()
                block_counts[block_type] = int(count)
            elif line.startswith("L"):
                _, x, y, vx, vy = line.split()
                lazors.append(((int(x), int(y)), (int(vx), int(vy))))
            elif line.startswith("P"):
                _, x, y = line.split()
                points.append((int(x), int(y)))

        # Fill missing block types with 0 to avoid KeyErrors later
        for block in ['A', 'B', 'C']:
            if block not in block_counts:
                block_counts[block] = 0

        return {
            "grid": grid,
            "block_counts": block_counts,
            "lazors": lazors,
            "points": points
        }
