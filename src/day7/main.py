import functools


def read_tachyon_map(filename) -> list[str]:
    with open(filename, "r") as file:
        tmap = file.read().split("\n")
    return tmap


def find_position(tmap: list[str], char="S") -> tuple[int, int]:
    for y, line in enumerate(tmap):
        x = line.find(char)
        if x > -1:
            return x, y
    return -1, -1


def get_beam_splits(filename: str) -> int:
    tmap = read_tachyon_map(filename)
    w = len(tmap[0])
    h = len(tmap)
    split_count = 0

    x, y = find_position(tmap, "S")

    def replace_char(y, x, new_char):
        tmap[y] = tmap[y][:x] + new_char + tmap[y][x + 1 :]

    for y in range(y + 1, h):
        for x in range(0, w):
            c = tmap[y][x]
            up = tmap[y - 1][x]
            new_char = None
            if c == ".":  # empty space continue what's above
                if up in ("S", "|"):
                    replace_char(y, x, "|")
            if c == "^":  # splitter
                if up in ("S", "|"):
                    split_count += 1
                    replace_char(y, x - 1, "|")
                    replace_char(y, x + 1, "|")
    return split_count


def get_quantum_beam_splits(filename: str) -> int:
    tmap = read_tachyon_map(filename)
    h = len(tmap)

    x, y = find_position(tmap, "S")

    @functools.cache
    def count_timelines(x, y):
        if y >= h:
            return 1
        c = tmap[y][x]

        if c == "^":
            left = count_timelines(x - 1, y + 1)
            right = count_timelines(x + 1, y + 1)
            return left + right
        else:
            return count_timelines(x, y + 1)  # just go down

    return count_timelines(x, y)


if __name__ == "__main__":
    assert get_beam_splits("sample.txt") == 21
    print("Part 1:", get_beam_splits("input.txt"))

    assert get_quantum_beam_splits("sample.txt") == 40
    print("Part 2:", get_quantum_beam_splits("input.txt"))
