from collections import defaultdict


def read_red_tiles(filename) -> list[tuple[int, int]]:
    with open(filename, "r") as file:
        lines = file.read().split("\n")
    return [tuple(map(int, line.split(",", 1))) for line in lines]


def get_biggest_red(filename: str) -> int:
    tiles = read_red_tiles(filename)
    max_size = 0
    for a in tiles:
        for b in tiles:
            if a != b:
                w = abs(a[0] - b[0]) + 1
                h = abs(a[1] - b[1]) + 1
                size = w * h
                if size > max_size:
                    max_size = size

    return max_size


class Map:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: list[list[str]] = [
            ["." for _ in range(width + 1)] for _ in range(height + 1)
        ]

    def set_tile(self, x, y, char):
        self.grid[y][x] = char

    def print(self):
        for line in self.grid:
            print("".join(line))

    def set_line(self, a, b, char):
        if a[0] == b[0]:  # vertical line
            x = a[0]
            for y in range(min(a[1], b[1]) + 1, max(a[1], b[1])):
                self.set_tile(x, y, char)
        elif a[1] == b[1]:  # horizontal line
            y = a[1]
            for x in range(min(a[0], b[0]) + 1, max(a[0], b[0])):
                self.set_tile(x, y, char)
        else:
            raise ValueError("Invalid direction")


def get_biggest_red_green_map(filename: str) -> int:
    """Here I was getting the MAP - but for the input this is too big to compute"""
    tiles = read_red_tiles(filename)
    max_x: int = max(t[0] for t in tiles)
    max_y: int = max(t[1] for t in tiles)
    print("Creating a map of size", max_x, "x", max_y)
    map = Map(max_x, max_y)
    for x, y in tiles:
        map.set_tile(x, y, "#")  # red
    for a, b in zip(tiles, tiles[1:] + tiles[:1]):
        map.set_line(a, b, "X")  # green
    map.print()
    return 40


class Polygon:
    def __init__(self, points: list[tuple[int, int]]):
        self.points: list[tuple[int, int]] = points
        self.min_x = min(p[0] for p in points)
        self.max_x = max(p[0] for p in points)
        self.min_y = min(p[1] for p in points)
        self.max_y = max(p[1] for p in points)
        self.lines = [(a, b) for a, b in zip(points, points[1:] + points[:1])]

    def sub_squares_by_size(self):
        squares_by_size = defaultdict(list)
        for a in self.points:
            for b in self.points:
                if a != b:
                    w = abs(a[0] - b[0]) + 1
                    h = abs(a[1] - b[1]) + 1
                    size = w * h
                    squares_by_size[size].append((a, b))  # we get all of them
        return squares_by_size

    def is_square_internal(self, a: tuple[int, int], b: tuple[int, int]) -> bool:
        # check the 4 corners
        min_x, max_x = min(a[0], b[0]), max(a[0], b[0])
        min_y, max_y = min(a[1], b[1]), max(a[1], b[1])

        corners = [
            (min_x, min_y),
            (min_x, max_y),
            (max_x, min_y),
            (max_x, max_y),
        ]

        # Check all rectangle corners are inside the polygon
        if not all(self.is_point_inside(c) for c in corners):
            return False

        # Check that no polygon vertices are strictly inside the rectangle
        # (vertices on the rectangle boundary are OK)
        for px, py in self.points:
            if min_x < px < max_x and min_y < py < max_y:
                return False

        # IMPORTANT: Also need to check that no polygon edges cross through the rectangle
        # An edge can pass through without having vertices inside!
        for (l1x, l1y), (l2x, l2y) in self.lines:
            # Check if this edge crosses through the rectangle interior
            # For horizontal/vertical edges, this is simpler
            if l1x == l2x:  # Vertical edge at x = l1x
                x = l1x
                if min_x < x < max_x:  # Edge is strictly inside horizontally
                    edge_min_y, edge_max_y = min(l1y, l2y), max(l1y, l2y)
                    # Check if edge passes through the rectangle vertically
                    # Edge crosses if: edge_min_y < max_y and edge_max_y > min_y
                    if edge_min_y < max_y and edge_max_y > min_y:
                        return False
            elif l1y == l2y:  # Horizontal edge at y = l1y
                y = l1y
                if min_y < y < max_y:  # Edge is strictly inside vertically
                    edge_min_x, edge_max_x = min(l1x, l2x), max(l1x, l2x)
                    # Check if edge passes through the rectangle horizontally
                    if edge_min_x < max_x and edge_max_x > min_x:
                        return False

        return True

    def is_point_inside(self, p):
        # to check if a point is inside the polygon we can use the ray-casting algorithm
        if p in self.points:
            return True

        x, y = p
        inside = False
        for (l1x, l1y), (l2x, l2y) in self.lines:
            # Check if the line crosses the horizontal ray at y
            if (l1y > y) != (l2y > y):
                # Calculate the x-coordinate where the line crosses y
                # Using linear interpolation: x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                x_intersection = l1x + (y - l1y) * (l2x - l1x) / (l2y - l1y)
                if x < x_intersection:
                    inside = not inside
        return inside


def get_biggest_red_green(filename: str) -> int | None:
    points = read_red_tiles(filename)
    polygon = Polygon(points)
    squares_by_size = polygon.sub_squares_by_size()

    for size in sorted(squares_by_size.keys(), reverse=True):
        for a, b in squares_by_size[size]:
            if polygon.is_square_internal(a, b):
                print(f"Choosing square {a} to {b} of size {size}")
                return size
    return None


if __name__ == "__main__":
    assert get_biggest_red("sample.txt") == 50
    print("Part 1:", get_biggest_red("input.txt"))

    assert get_biggest_red_green("sample.txt") == 24
    print("Part 2:", get_biggest_red_green("input.txt"))
