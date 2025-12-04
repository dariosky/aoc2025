def read_map(filename) -> list[str]:
    with open(filename, "r") as file:
        map = [line.strip() for line in file.readlines()]
    return map


def find_available_forklifts(filename, replace=False) -> int:
    fork_map = read_map(filename)
    max_y = len(fork_map) - 1
    max_x = len(fork_map[0]) - 1

    def reachable_forklift(x, y):
        adjacents = 0
        if y > 0:
            if x > 0 and fork_map[y - 1][x - 1] == "@":  # NW
                adjacents += 1
            if fork_map[y - 1][x] == "@":  # N
                adjacents += 1
            if x < max_x and fork_map[y - 1][x + 1] == "@":  # NE
                adjacents += 1

        if x > 0 and fork_map[y][x - 1] == "@":  # W
            adjacents += 1
        if x < max_x and fork_map[y][x + 1] == "@":  # E
            adjacents += 1

        if y < max_y:
            if x > 0 and fork_map[y + 1][x - 1] == "@":  # SW
                adjacents += 1
            if fork_map[y + 1][x] == "@":  # S
                adjacents += 1
            if x < max_x and fork_map[y + 1][x + 1] == "@":  # SE
                adjacents += 1

        return adjacents < 4

    accessible = 0
    while True:
        one_step_accessible = 0
        for y, line in enumerate(fork_map):  # very simple, quadratic search
            for x, c in enumerate(line):
                if c == "@" and reachable_forklift(x, y):
                    one_step_accessible += 1
                    if replace:
                        line = line[:x] + "x" + line[x + 1 :]
                        fork_map[y] = line
        accessible += one_step_accessible
        if not replace or not one_step_accessible:
            break
    return accessible


if __name__ == "__main__":
    assert find_available_forklifts("sample.txt") == 13
    print("Part 1:", find_available_forklifts("input.txt"))

    assert find_available_forklifts("sample.txt", replace=True) == 43
    print("Part 2:", find_available_forklifts("input.txt", replace=True))
