demo = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

inp = demo
inp = open('input.txt').read()
grid = inp.split('\n')[:-1]
row_max = len(grid)-1
col_max = len(grid[0])-1

solution1 = 0
solution2 = 0
num = ''
start = 999
end = 0

def findAny(subarr):
    for idx, el in enumerate(subarr):
        if el in ['*', '/', '=', '-', '&', '%', '$', '+', '#', '@']:
            return True, el, idx
    return False, 0, 0

def checkIfAdjacentWithSymbol(r, start, end, grid):
    max_start = max(0, start-1)
    min_end = min(col_max+1, end+1)

    # check above
    if (r - 1) >= 0:
        subarr = grid[r-1][max_start:min_end]
        check, el, idx = findAny(subarr)
        if check:
            return True, (el, (r-1, max_start+idx))

    # check below
    if (r + 1) <= row_max:
        subarr = grid[r+1][max_start:min_end]
        check, el, idx = findAny(subarr)
        if check:
            return True, (el, (r+1, max_start+idx))

    # check middle
    subarr = grid[r][max_start:min_end]
    check, el, idx = findAny(subarr)
    if check:
        return True, (el, (r, max_start+idx))

    return False, ()

from collections import defaultdict
from functools import reduce
gear_map = defaultdict(list)
for r, row in enumerate(grid):
    for c, col in enumerate(row):
        if col in ['.', '*', '/', '=', '-', '&', '%', '$', '+', '#', '@']:
            if num != '':
                check, el = checkIfAdjacentWithSymbol(r, start, c, grid)
                if check:
                    solution1 += int(num)
                    if el[0] == '*':
                        gear_map[el[1]].append(int(num))
            num = ''
            start = 999
            end = 0
            continue
        num += col
        start = min(c, start)

    check, el = checkIfAdjacentWithSymbol(r, start, col_max, grid)
    if num != '' and check:
        solution1 += int(num)
        if el[0] == '*':
            gear_map[el[1]].append(int(num))

        num = ''
        start = 999
        end = 0

solution2 = 0
for gears in gear_map.values():
    if len(gears) < 2:
        continue
    solution2 += reduce(lambda x, y: x*y, gears)

print('----------------')
print(solution1)
print(solution2)

