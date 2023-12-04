
demo = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

from collections import deque
inp = demo
inp = open('input.txt').read()
inp = inp.splitlines()

col_size = len(inp[0])
row_size = len(inp)
start_pos = (0,1)
end_pos = (row_size-1, col_size-2)

dir_to_num = {
  '>': 0,
  'v': 1,
  '<': 2,
  '^': 3
}

dir_to_chr = {
  0: '>',
  1: 'v',
  2: '<',
  3: '^'
}

# blizz (row, col, direction)
blizz_ptr = []
wall_dict = {}
for row in range(row_size):
  for col in range(col_size):
    el = inp[row][col]
    if el != '#' and el != '.':
      blizz_ptr.append((row, col, dir_to_num[el]))

    if el == '#':
      wall_dict[(row, col)] = '#'

def create_dir_dicts(blizz):
  # [right, down, left, up]
  list_dict = [{}, {}, {}, {}]
  for idx, (row, col, el) in enumerate(blizz):
    list_dict[el][(row, col)] = idx

  return list_dict

def print_grid(list_dir, wall, elves):
  for row in range(row_size):
    for col in range(col_size):
      el = ''
      num = 0
      if (row, col) in list_dir[0]:
        el = '>'
        num += 1
      if (row, col) in list_dir[1]:
        el = 'v'
        num += 1
      if (row, col) in list_dir[2]:
        el = '<'
        num += 1
      if (row, col) in list_dir[3]:
        el = '^'
        num += 1

      if num == 1:
        print(el, end='')
      elif num > 1:
        print(num, end='')
  
      elif (row, col) in wall:
        print(wall[(row, col)], end='')
      elif (row, col) == elves:
        print('E', end='')
      else:  
        print('.', end='')
    print('')

def calculate_next_minute(blizz_ptr):
  new_blizz_ptr = []
  for row, col, el in blizz_ptr:
    if el == 0:
      if (col+2) < col_size:
        new_blizz_ptr.append((row, col+1, el))
      else:
        new_blizz_ptr.append((row, 1, el))

    elif el == 1:
      if (row+2) < row_size:
        new_blizz_ptr.append((row+1, col, el))
      else:
        new_blizz_ptr.append((1, col, el))

    elif el == 2:
      if (col-1) < 1:
        new_blizz_ptr.append((row, col_size-2, el))
      else:
        new_blizz_ptr.append((row, col-1, el))
    elif el == 3:
      if (row-1) < 1:
        new_blizz_ptr.append((row_size-2, col, el))
      else:
        new_blizz_ptr.append((row-1, col, el))
    
  return new_blizz_ptr

def find_possible_move(elves, l_dir, wall):
  # right, down, left, up
  d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
  moves = []
  for (r, c) in d:
    r_d = elves[0]+r
    c_d = elves[1]+c
    if (r_d, c_d) in wall:
      continue
  
    if ((r_d < 0) or (r_d >= row_size)):
      continue

    free = True
    for dir in l_dir:
      if (r_d, c_d) in dir:
        free = False
        break
    
    if free:
      moves.append((r_d, c_d))
  moves.append((elves))
  return moves

def isElfDead(elf_pos, l_dir):
  dead = False
  for dir in l_dir:
    if elf_pos in dir:
      dead = True
      break
  return dead

#start_pos, blizz_ptr, list_dir, wall_dict
def BFS(s_p, b_p, wall, end_pos):
  queue = deque()
  l_d = create_dir_dicts(b_p)
  b_f = b_p
  time = 1

  onLoop = True
  goToEnd = True

  visited = set()
  pos_move = []

  sol1 = 0
  sol2 = 0
  b_f = calculate_next_minute(b_f)
  l_d = create_dir_dicts(b_f)
  pos_move = find_possible_move(s_p, l_d, wall)
    
  for pos in pos_move:
    queue.append((time, pos, b_f, l_d))

  while len(queue):
    time, pos, b_p, l_d = queue.popleft()
    if isElfDead(pos, l_d):
        continue
    if (time,pos) in visited:
     continue

    visited.add((time, pos))
    if goToEnd:
      if not onLoop and (pos == end_pos):
        sol2 = time
        break

      if (pos == end_pos) and onLoop:
        goToEnd = False
        onLoop = False
        visited = set()
        queue = deque()
        sol1 = time
    else:
      if pos == s_p:
        goToEnd = True
        visited = set()
        queue = deque()
 
    b_f = b_p 
    b_f = calculate_next_minute(b_f)
    l_d = create_dir_dicts(b_f)
    pos_move = find_possible_move(pos, l_d, wall)
    time+=1

    for p in pos_move:
      queue.append((time, p, b_f, l_d))

  return sol1, sol2

s1, s2 = BFS(start_pos, blizz_ptr, wall_dict, end_pos)

print(f'Solution1: {s1}')
print(f'Solution2: {s2}')
