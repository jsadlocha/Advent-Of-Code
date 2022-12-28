demo = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

import re
inp = demo
inp = open('/home/hardware/Workspace/Advent-Of-Code-2022/Day22/input.txt').read()

inp = inp.splitlines()

maze = inp[:-2]
path_org = inp[-1]


start_row = 1
start_col = 0
start_dir = 0
for i, el in enumerate(maze[0]):
  if el == '.':
    start_col = i+1
    break

max_width = 0
max_height = len(maze)
for i in maze:
  max_width = max(max_width, len(i))

# (num, rotate)
pattern = r'(\d+)(\w?)'
path = re.findall(pattern, path_org)

grid = []
grid.append([' ']*max_width+[' ']*2)
for i in range(max_height):
  grid.append([' ']+list(maze[i])+[' ']*(max_width-(len(maze[i])-1)))
grid.append([' ']*max_width+[' ']*2)


for i in grid:
  max_width = max(max_width, len(i))

max_height = len(grid)

def print_grid(grid):
  for row in grid:
    for col in row:
      print(col, end='')
    print('')

# directions
# 0 - right
# 1 - down
# 2 - left
# 3 - up

s_dir = {0: '>', 1: 'v', 2: '<', 3: '^'}

# trawerse grid
r = start_row
c = start_col
d = start_dir
for moves, dir in path:
  _c = c
  _r = r
  for i in range(int(moves)):
    # grid[_r][_c] = s_dir[d]
    old_c = _c
    old_r = _r
    if d == 0:
      _c += 1
    elif d == 1:
      _r += 1
    elif d == 2:
      _c -= 1
    elif d == 3:
      _r -= 1

    if grid[_r][_c] == ' ':
      if d == 0: # right
        for j in range(max_width-1):
          if grid[_r][j] != ' ':
            _c = j
            break

      if d == 2: # left
        for j in range(max_width-1, -1, -1):
          if grid[_r][j] != ' ':
            _c = j
            break

      if d == 1: # down
        for j in range(max_height-1):
          if grid[j][_c] != ' ':
            _r = j
            break

      if d == 3: # up
        for j in range(max_height-1, -1, -1):
          if grid[j][_c] != ' ':
            _r = j
            break

    if grid[_r][_c] == '#':
      _c = old_c
      _r = old_r
      break

    c = _c
    r = _r
    grid[r][c] = s_dir[d]
  
  if dir == 'R':
    d = (d+1) % 4
  elif dir == 'L':
    d = (d-1) % 4


# print_grid(grid)

sol1 = (1000*r)+(4*c)+d

# trawerse grid
r = start_row
c = start_col
d = start_dir

for moves, dir in path:
  _c = c
  _r = r
  for i in range(int(moves)):
    # grid[_r][_c] = s_dir[d]
    old_c = _c
    old_r = _r
    old_d = d
    if d == 0:
      _c += 1
    elif d == 1:
      _r += 1
    elif d == 2:
      _c -= 1
    elif d == 3:
      _r -= 1

    if grid[_r][_c] == ' ':
      # U
      if 51 <= c and 100 >= c and 1 <= r and 50 >= r:
        if _r < 1:
          _r = (c-50)+150
          _c = 1
          d = 0
        elif _c < 51:
          _r = 151-r
          _c = 1
          d = 0

      # R
      elif 101 <= c and 150 >= c and 1 <= r and 50 >= r:
        if _r < 1:
          _c = c-100
          _r = 200
          d = 3

        elif _c > 150:
          _r = 151-r
          _c = 100
          d = 2

        elif _r > 50:
          _r = c-100+50
          _c = 100
          d = 2

      # F
      elif 51 <= c and 100 >= c and 51 <= r and 100 >= r:
        if _c < 51:
          _c = r-50
          _r = 101
          d = 1

        elif _c > 100:
          _c = _r+50#-50+100
          _r = 50
          d = 3

      # D
      elif 51 <= c and 100 >= c and 101 <= r and 150 >= r:
        if _c > 100:
          _r = 51-(r-100)
          _c = 150
          d = 2

        elif _r > 150:
          _r = (c-50)+150
          _c = 50
          d = 2

      # L
      elif 1 <= c and 50 >= c and 101 <= r and 150 >= r:
        if _r < 101:
          _r = c+50
          _c = 51
          d = 0

        elif _c < 1:
          _r = 51-(r-100)
          _c = 51
          d = 0

      # B
      elif 1 <= c and 50 >= c and 151 <= r and 200 >= r:
        if _c < 1:
          _c = (r-150)+50
          _r = 1
          d = 1

        elif _c > 50:
          _c = r-150+50
          _r = 150
          d = 3

        elif _r > 200:
          _c = c+100
          _r = 1
          d = 1

    if grid[_r][_c] == '#':
      _c = old_c
      _r = old_r
      d = old_d
      break  

    c = _c
    r = _r
    grid[r][c] = s_dir[d]
  
  if dir == 'R':
    d = (d+1) % 4
  elif dir == 'L':
    d = (d-1) % 4


# print_grid(grid)
sol2 = (1000*r)+(4*c)+d

print(f'Solution1: {sol1}')
print(f'Solution2: {sol2}')