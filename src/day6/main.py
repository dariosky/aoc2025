import re


def read_columns(filename) -> list[list[str | int]]:
    columns = []
    with open(filename, "r") as file:
        for line in file.readlines():
            row = re.split(r"\s+", line.strip())
            if not columns:
                columns = [[value] for value in row]  # create columns
            else:
                for col, value in enumerate(row):
                    columns[col].append(value)

    return [  # map the numbers
        list(map(int, column[:-1])) + [column[-1]] for column in columns
    ]


def sum_results(filename: str, parser=read_columns) -> int:
    columns = parser(filename)

    def compute_column(column: list[str | int]) -> int:
        operator_map = {
            "*": lambda a, b: a * b,
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "/": lambda a, b: a // b,
        }
        operator = column[-1]
        total = column[0]
        for number in column[1:-1]:  # from 2nd to 2nd last
            total = operator_map[operator](total, number)
        return total

    return sum(compute_column(column) for column in columns)


def read_strict_columns(filename) -> list[list[str | int]]:
    """Read as columns with strict one space separation"""
    with open(filename, "r") as file:
        lines = list(map(lambda s: s.rstrip("\n"), file.readlines()))
    operators = re.split(r"\s+", lines[-1].strip())
    str_columns: list[str] = []
    for line in lines[:-1]:
        if not str_columns:
            for value in line:
                str_columns.append(value if value != " " else "")
        else:
            for x, value in enumerate(line):
                if value != " ":
                    str_columns[x] = str_columns[x] + value
    columns = []
    column = []
    for str_column in str_columns:
        if str_column == "":
            columns.append(column)
            column = []
        else:
            column.append(int(str_column))
    columns.append(column)
    for x, operator in enumerate(operators):
        columns[x].append(operator)
    return columns


if __name__ == "__main__":
    assert sum_results("sample.txt") == 4277556
    print("Part 1:", sum_results("input.txt"))

    assert sum_results("sample.txt", parser=read_strict_columns) == 3263827
    print("Part 2:", sum_results("input.txt", parser=read_strict_columns))
