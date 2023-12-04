
demo = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

from collections import deque
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

def hash_func(grid, top, max_row, new_top):
  lookup = {'.': 0, '#': 1}
  hash_sum = 0
  for idx in range(top-max_row, top):
    for col in range(len(grid[0])):
      hash_sum *= 2
      hash_sum += lookup[grid[idx][col]]
  return hash_sum % (2**64+1)

empty_line = ['.......']
# grid_parse = empty_line+grid_parse

def solve_hight(rooks_number, red_flag):
  # change grid to list
  lookup_table = {}
  rk_num = 0
  grid2 = []
  for line in grid_parse:
    grid2.append(list(line))

  new_rook_number = 0
  new_high_top = 0
  last_high_top = 0
  row_offset = start_row
  row_offset_global = 3
  col_offset = start_col
  col_offset_global = 2
  start_offset_global = 3
  wind_idx = 0
  high_point = 0
  old_rooks = 0
  old_high_point = 0
  for i in range(rooks_number): 
    new_rook_number += 1
    if new_rook_number >= rooks_number:
     break
    
    
    rk_num += 1
    if rk_num == rooks_number:
      break

    b = blk_elements[i % 5]
    row_offset_global = start_offset_global
    col_offset = col_offset_global
    
    for i in range(start_offset_global+blk_width[i%5] - len(grid2)):
      grid2 = grid2 + [list('.......')]
    
    row_offset = row_offset_global
    
    # brick falling
    while True:    
      wind_offset_col = 0
      if wind[wind_idx] == '>':
        wind_offset_col = 1
      else:
        wind_offset_col = -1
      
      old_col = col_offset
      if precheck(grid2, b, row_offset, col_offset+wind_offset_col):
        col_offset+=wind_offset_col

      
      # precheck
      move_possible = precheck(grid2, b, row_offset-1, col_offset)
      if move_possible:
        row_offset-=1

      
      wind_idx += 1
      wind_idx %= len(wind)
      
      if move_possible == False:
        break

   
    for row, col in b:
      high_point = max(high_point, row+row_offset)
      grid2[row+row_offset][col+col_offset] = '#'
    
    start_offset_global = high_point +4

    if red_flag:
      if rk_num > 20:
        if lookup_table.get((hash_func(grid2, high_point, 20, 0), wind_idx)):
          
          last_high, num_rooks = lookup_table[(hash_func(grid2, high_point, 20, 0), wind_idx)]
          diff = high_point-last_high
          diff_rook = rk_num - num_rooks
          old_rooks = rk_num
          old_high_point = high_point
        
          new_rook_number = rk_num
          new_high_top = high_point
          remaining_rooks = rooks_number
          ex = True
          while ex:
            times = remaining_rooks//diff_rook 
            if remaining_rooks < 20:
              ex = False
             
            
            new_rook_number = new_rook_number+(diff_rook*times)
            new_high_top = new_high_top+(diff*times)

            
            last_high_top = high_point
            remaining_rooks -= diff_rook * times
          
          
       
          new_rook_number -= diff_rook*2
          new_high_top-=diff*2
    
          red_flag = False
        else:
          lookup_table[(hash_func(grid2, high_point, 20, new_high_top), wind_idx)] = (high_point, rk_num)
    
  

  return new_high_top+high_point-old_high_point+1

fall_number = 1_000_000_000_000
print(f'Solution1: {solve_hight(2023, False)}')
print(f'Solution2: {solve_hight(1_000_000_000_001, True)}')
