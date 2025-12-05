def read_ingredients(filename) -> tuple[list[tuple[int, int]], set[str]]:
    ranges = []
    available = set()
    with open(filename, "r") as file:
        lines = file.readlines()
        get = "ranges"
        for line in lines:
            line = line.strip()
            if not line:
                get = "available"
                continue
            if get == "ranges":
                ranges.append(tuple(map(int, line.split("-"))))
            else:
                available.add(int(line))

    return ranges, available


def find_available_fresh(filename) -> int:
    fresh_available = 0
    ranges, available = read_ingredients(filename)
    for ingredient in available:
        for range in ranges:
            if range[0] <= ingredient <= range[1]:
                break
        else:
            continue
        fresh_available += 1

    return fresh_available


def find_fresh_naive(filename) -> int:
    ranges, _ = read_ingredients(filename)
    fresh_items = set()
    # the naive approach of adding all items in a set and then count
    # doesn't work for the input
    for r in ranges:
        for item in range(r[0], r[1] + 1):
            fresh_items.add(item)
    return len(fresh_items)


def find_fresh(filename) -> int:
    def remove_overlap(sorted_ranges: list[tuple[int, int]]) -> tuple[int, int]:
        results = []
        previous_start, previous_end = None, None
        for i, (start, end) in enumerate(sorted_ranges):
            if previous_start is None:  # skip the first
                previous_start, previous_end = start, end
                continue
            if start > previous_end:  # we have a gap
                results.append((previous_start, previous_end))
                previous_start, previous_end = start, end
            else:
                previous_end = max(end, previous_end)  # extend the previous end

        results.append((previous_start, previous_end))  # add the last
        return results

    ranges, _ = read_ingredients(filename)
    # instead of counting items in a range we just create a set of ranges
    # that are not overlapping - and then count
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    final_ranges = remove_overlap(sorted_ranges)
    fresh_count = 0
    for start, end in final_ranges:
        fresh_count += end - start + 1
    return fresh_count


if __name__ == "__main__":
    assert find_available_fresh("sample.txt") == 3
    print("Part 1:", find_available_fresh("input.txt"))

    assert find_fresh("sample.txt") == 14
    print("Part 2:", find_fresh("input.txt"))
