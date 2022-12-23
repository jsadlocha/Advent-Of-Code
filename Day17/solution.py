
demo = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

import copy
inp = demo
inp = open('input.txt').read()
wind = inp[:-1]



blk_elements = []
blk_width = []

# platform
blk_elements.append([(0, 0),(0, 1),(0, 2),(0, 3)])
blk_width.append(1)

# cross
blk_elements.append([(0,1),
              (1,0),(1,1),(1,2),
              (2,1)])
blk_width.append(3)

# reverse L
blk_elements.append([(2,2),
              (1,2),
              (0,0), (0,1),(0,2)])
blk_width.append(3)

# column
blk_elements.append([(3,0),
              (2,0),
              (1,0),
              (0,0)])
blk_width.append(4)

# brick
blk_elements.append([(1,0),(1,1),
              (0,0),(0,1)])
blk_width.append(2)

start_col = 2
start_row = 3

# basic print debug 
def printBlocks(blk, blk_width, row_max=2, col_max=7):
  for i, b in enumerate(blk):
    for row in range(row_max+blk_width[i], -1, -1):
      for col in range(0, col_max):
        if col == 0:
          print('|', end='')
        if (row-start_row, col-start_col) in b:
          print('@', end='')
        else:
          print('.', end='')
        if col == 6:
          print('|', end='')
      print('')
    print('+-------+')

# printBlocks(blk_elements, blk_width)

grid_parse = """.......
.......
.......
""".splitlines()

def printGrid(grid):
  print('+-------+')
  for idx, line in enumerate(grid[::-1]):
    for idx, el in enumerate(line):
      if idx == 0:
        print('|',end='')
      print(el, end='')
      if idx == 6:
        print('|', end='')
    print('')
  print('+-------+')
  

def drawBrick(brick, brick_size):
  s = []
  for row in range(brick_size-1, -1, -1):
    rs = ''
    for col in range(0, 7):
      if (row, col-start_col) in brick:
        rs += '@'
      else:
        rs += '.'
    s.append(rs)
  return s

# b = drawBrick(blk_elements[2], blk_width[2])
# printGrid(b+grid_parse)

def precheck(grid, brick, row_offset, col_offset):
  move_possible = True
  for row, col in brick:
      if (col+col_offset) > 6 or (col+col_offset) < 0:
        move_possible = False
        break
      if (row+row_offset) < 0:
        move_possible = False
        break
      el = grid[row+row_offset][col+col_offset]
      if el != '.':
        move_possible = False
        break
  return move_possible

empty_line = ['.......']
# grid_parse = empty_line+grid_parse

# change grid to list
grid2 = []
for line in grid_parse:
  grid2.append(list(line))

row_offset = start_row
row_offset_global = 3
col_offset = start_col
col_offset_global = 2
start_offset_global = 3
wind_idx = 0
high_point = 0
for i in range(2022):
  b = blk_elements[i % 5]
  row_offset_global = start_offset_global
  col_offset = col_offset_global
  
  for i in range(start_offset_global+blk_width[i%5] - len(grid2)):
    grid2 = grid2 + [list('.......')]
  
  row_offset = row_offset_global
  
  # #draw on grid debug
  # grid3 = copy.deepcopy(grid2)
  # #printGrid(grid3)
  # for row, col in b:
  #   grid3[row+row_offset][col+col_offset] = '#'
  # printGrid(grid3)

  # brick falling
  while True:    
    wind_offset_col = 0
    if wind[wind_idx] == '>':
      wind_offset_col = 1
    else:
      wind_offset_col = -1
    
    # print('before wind')
    # # draw on grid debug
    # grid3 = copy.deepcopy(grid2)
    # #printGrid(grid3)
    # for row, col in b:
    #   # print(f'row: {row} col {col}')
    #   # print(len(grid3))
    #   # print(len(grid3[0]))
    #   grid3[row+row_offset][col+col_offset] = '#'
    # printGrid(grid3)
    
    old_col = col_offset
    if precheck(grid2, b, row_offset, col_offset+wind_offset_col):
      col_offset+=wind_offset_col

    # print('after wind')
    # # draw on grid debug
    # grid3 = copy.deepcopy(grid2)
    # #printGrid(grid3)
    # for row, col in b:
    #   #print(f'row: {row} col {col}')
    #   grid3[row+row_offset][col+col_offset] = '#'
    # printGrid(grid3)
    
    # precheck
    move_possible = precheck(grid2, b, row_offset-1, col_offset)
    if move_possible:
      row_offset-=1

    # print('after move')
    # # draw on grid debug
    # grid3 = copy.deepcopy(grid2)
    # #printGrid(grid3)
    # for row, col in b:
    #   #print(f'row: {row} col {col}')
    #   grid3[row+row_offset][col+col_offset] = '#'
    # printGrid(grid3)
    
    
    wind_idx += 1
    wind_idx %= len(wind)

    if move_possible == False:
      break

  #highest point
  max_row = 0
  for row, col in b:
    max_row = max(row+row_offset, max_row)
  

  #draw on grid debug
  #grid3 = copy.deepcopy(grid2)
  # print(b)
  # print(row_offset)
  # print(col_offset)
  for row, col in b:
    high_point = max(high_point, row+row_offset)
    #print(high_point)
    grid2[row+row_offset][col+col_offset] = '#'
    # grid2[row][col] = '#'
  # printGrid(grid2)
  start_offset_global = high_point +4
  # print('next')
  # break
printGrid(grid2)
print(len(grid2))
print(f'Solution1: {high_point+1}')



