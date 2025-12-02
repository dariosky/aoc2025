def read_ranges(filename) -> list[tuple[int, int]]:
    with open(filename, "r") as file:
        content = file.read()
        ranges = [
            (int(range_start), int(range_end))
            for range_start, range_end in [
                line.split("-") for line in content.split(",")
            ]
        ]
    return ranges


def sum_invalid_ids(filename) -> int:
    result = 0
    ranges = read_ranges(filename)

    # iterate through all invalid ids from 11 to the max
    max_range = max(range_end for _, range_end in ranges)
    candidate_half = 1
    while True:
        candidate_str = str(candidate_half) * 2
        candidate = int(candidate_str)
        if candidate > max_range:
            break
        for range_start, range_end in ranges:
            if range_start <= candidate <= range_end:
                # print(
                #     f"Found candidate {candidate} in range {range_start}-{range_end}"
                # )
                result += candidate
        candidate_half += 1

    return result


def sum_invalid_sillier_ids(filename) -> int:
    invalid_ids = set()
    ranges = read_ranges(filename)
    # iterate through all invalid ids from 11 to the max
    max_range = max(range_end for _, range_end in ranges)
    max_range_str = str(max_range)
    candidate_part = 1
    while True:
        # for each candidate_part
        candidate_part_str = str(candidate_part)
        max_repetitions = len(max_range_str) // len(candidate_part_str)

        # for the repetitions
        for repetitions in range(2, max_repetitions + 1):
            candidate_str = candidate_part_str * repetitions

            candidate = int(candidate_str)
            if candidate > max_range:
                break
            for range_start, range_end in ranges:
                if range_start <= candidate <= range_end:
                    invalid_ids.add(candidate)  # deduplicated
        candidate_part += 1
        if len(candidate_part_str) * 2 > len(max_range_str):
            break
    return sum(invalid_ids)


if __name__ == "__main__":
    assert sum_invalid_ids("sample.txt") == 1227775554
    print("Part 1:", sum_invalid_ids("input.txt"))

    assert sum_invalid_sillier_ids("sample.txt") == 4174379265
    print("Part 2:", sum_invalid_sillier_ids("input.txt"))
