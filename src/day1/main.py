INITIAL_POSITION = 50


def compute_code(filename) -> int:
    zero_positions = 0
    position = INITIAL_POSITION
    with open(filename, "r") as file:
        for line in file:
            direction, steps = line[0], int(line[1:])
            steps = steps if direction == "R" else -steps
            position = (position + steps) % 100
            if position == 0:
                zero_positions += 1

    return zero_positions


def compute_code_with_ticks(filename) -> int:
    zero_positions = 0
    position = INITIAL_POSITION
    with open(filename, "r") as file:
        for line in file:
            direction, steps = line[0], int(line[1:])
            for _ in range(steps):
                position = (position + (1 if direction == "R" else -1)) % 100
                if position == 0:
                    zero_positions += 1

    return zero_positions


if __name__ == "__main__":
    assert compute_code("sample.txt") == 3
    print("Part 1:", compute_code("input.txt"))

    assert compute_code_with_ticks("sample.txt") == 6
    print("Part 2:", compute_code_with_ticks("input.txt"))
