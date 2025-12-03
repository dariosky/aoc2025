def read_jolts(filename) -> list[list[int]]:
    with open(filename, "r") as file:
        banks = [list(map(int, line.strip())) for line in file.readlines()]
    return banks


def bank_to_number(bank: list[int]) -> int:
    return sum(n * 10**i for i, n in enumerate(bank[::-1]))


def higher_jolts(bank: list[int], size: int) -> list[int]:
    extras = bank[: len(bank) - size + 1]
    # rule is: I need the higher and leftmost number of the extra part
    higher_msn = max(extras)
    index = extras.index(higher_msn)
    if size == 1:
        return [higher_msn]
    else:
        return [higher_msn] + higher_jolts(bank[index + 1 :], size - 1)


def find_higher_jolts_sum_recursive(filename, size=2) -> int:
    result = 0
    banks = read_jolts(filename)
    for b in banks:
        result += bank_to_number(higher_jolts(b, size))
    return result


def find_higher_jolts_sum(filename) -> int:
    result = 0
    banks = read_jolts(filename)

    for b in banks:  # very simple, quadratic search
        max_jolt = 0
        for x, first in enumerate(b):
            for second in b[x + 1 :]:
                if (value := first * 10 + second) > max_jolt:
                    max_jolt = value
        result += max_jolt
    return result


if __name__ == "__main__":
    assert find_higher_jolts_sum("sample.txt") == 357
    print("Part 1:", find_higher_jolts_sum("input.txt"))

    assert find_higher_jolts_sum_recursive("sample.txt", size=2) == 357
    assert find_higher_jolts_sum_recursive("input.txt", size=2) == 17324
    assert find_higher_jolts_sum_recursive("sample.txt", size=12) == 3121910778619
    print("Part 2:", find_higher_jolts_sum_recursive("input.txt", size=12))
