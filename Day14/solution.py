
demo = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

import re
import copy
# inp = demo.splitlines()
inp = open('/home/hardware/Workspace/Advent-Of-Code-2022/Day14/input.txt').read().splitlines()

def make_grid(inp):
  grid = []
  min_x = 10**12
  max_x = 0
  min_y = 0
  max_y = 0
  for l in inp:
    parsed = re.findall(r'\d+,\d+', l)
    it = iter(parsed)
    x_, y_ = map(int, next(it).split(','))
    for i in it:
      x, y = map(int, i.split(','))
      if x_ == x:
        if y_ < y:
          lo2, hi2 = y_, y+1
        else:
          lo2, hi2 = y, y_+1
        for c in range(lo2, hi2):
          grid.append((x,c))
          min_x = min(min_x, x)
          max_x = max(max_x, x)
          max_y = max(max_y, c)

      elif y_ == y:
        if x_ < x:
          lo, hi = x_, x+1
        else:
          lo, hi = x, x_+1
        for r in range(lo, hi):
          grid.append((r,y))
          min_x = min(min_x, r)
          max_x = max(max_x, r)
          max_y = max(max_y, y)
   
      x_, y_ = x, y
  return set(grid), (min_x, max_x), (min_y, max_y)
      
def print_grid(grid, x_range, y_range):
  print(f'x range {x_range}')
  print(f'y range {y_range}')

  for row in range(y_range[0], y_range[1]+1):
    for col in range(x_range[0], x_range[1]+1):
      if (col, row) in grid:
        print('#', end='')
      else:
        print('.', end='')
    print('')

def calculate_sand(grid, sand, x_range, y_range, solution1):
  x, y = sand
  t = 0
  while True:
    if solution1:
      if x > x_range[1] or x < x_range[0] or y > y_range[1]:
        break
      

    if (x, y+1) not in grid and y <= y_range[1]:
      y+=1
      continue

    if (x-1, y+1) not in grid and y <= y_range[1]:
      x-=1
      y+=1
      continue

    if (x+1, y+1) not in grid and y <= y_range[1]:
      x+=1
      y+=1
      continue

    if (x, y) not in grid or y > y_range[1]:
      t+=1
      grid.add((x,y))
      x, y = sand
      continue

    if (x, y) == sand:
      break

  return t

sand = (500, 0)
grid, x_range, y_range = make_grid(inp)
grid2 = copy.copy(grid)

t = calculate_sand(grid, sand, x_range, y_range, True)
print(f'Solution1: {t}')
t2 = calculate_sand(grid2, sand, x_range, y_range, False)
print(f'Solution2: {t2}')
