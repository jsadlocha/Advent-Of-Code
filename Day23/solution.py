demo1 = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
demo = """.....
..##.
..#..
.....
..##.
.....
"""


inp = demo1
inp = open('input.txt').read()
inp = inp.splitlines()
import copy

class Elves:
  def __init__(self, r, c, d):
    self.r = r
    self.c = c
    self.d = d

def parse_elves(data):
  elves = []
  for i in range(len(data)):
    for j in range(len(data[i])):
      if data[i][j] == '#':
        elves.append(Elves(i, j, 0))
  return elves

def minxy_maxxy(elves):
  x, y = 999999, 999999
  x2, y2 = -999999, -999999
  for e in elves:
    x_, y_ = e.r, e.c
    x = min(x, x_)
    y = min(y, y_)
    x2 = max(x2, x_)
    y2 = max(y2, y_)
  return x, y, x2, y2

def draw_grid(elves):
  mx, my, Mx, My = minxy_maxxy(elves)
  for r in range(mx, Mx+1):
    for c in range(my, My+1):
      for e in elves:
        if e.r == r and e.c == c:
          print('#', end='')
          break
      else:
        print('.', end='')
    print('')

nswe = [[(-1, 0), (-1, -1), (-1, 1)], # north
        [(1, 0), (1, -1), (1, 1)], # south
        [(-1, -1), (0, -1), (1, -1)],#, # west
        [(-1, 1), (0, 1),(1, 1)]] # east

direction = {0: (-1, 0),
             1: (1, 0),
             2: (0, -1),
             3: (0, 1)}

elves = parse_elves(inp)

def check_if_alone(elv, elv_list, nswe):
  alone = True
  for d in nswe:
    for r, c in d:
      for elv_test in elv_list:
        if (elv.r+r) == elv_test.r and (elv.c+c)== elv_test.c:
          alone = False
          break
  return alone

def check_if_mov_available(elv, elv_list, nswe):
  for i in range(4):
    space = True
    for r,c in nswe[(elv.d+i)%4]:
      for e in elv_list:
        if elv.r+r == e.r and elv.c+c == e.c:
          space = False
          break
    if space:
      return True
  
  return space
    

def get_proposed_move(elv, elv_list, nswe, dir_):
  for i in range(4):
    ok = True
    for r,c in nswe[(elv.d+i)%4]:
      for e in elv_list:
        if elv.r+r == e.r and elv.c+c == e.c:
          ok = False
          break
    if ok:
      r_, c_ = dir_[(elv.d+i)%4]
      return (elv.r+r_, elv.c+c_, elv.d) 

  print('this cannot be print!')
  return ()

def calc_empty_space(elves):
  mx, my, Mx, My = minxy_maxxy(elves)
  count = 0
  for r in range(mx, Mx+1):
    for c in range(my, My+1):
      for e in elves:
        if e.r == r and e.c == c:
          break
      else:
        count+=1
  return count

solution1 = 0
solution2 = 0
for time in range(10000):
  print(f'{time}')
  proposed = []
  new_elfs = copy.deepcopy(elves)

  for elv in elves:
    if not check_if_alone(elv, elves, nswe):
      break
  else:
    solution2 = time+1
    break


  for elv in elves:
    if check_if_alone(elv, elves, nswe):
      continue
    if not check_if_mov_available(elv, elves, nswe):
      continue

    x, y, d = get_proposed_move(elv, elves, nswe, direction)
    proposed.append((x,y))

  for elf_id, elv in enumerate(elves):
    if check_if_alone(elv, elves, nswe):
      new_elfs[elf_id].d = (d+1) % 4
      continue
    if not check_if_mov_available(elv, elves, nswe):
      new_elfs[elf_id].d = (d+1) % 4
      continue
    p_ = proposed[:]
    x, y, d = get_proposed_move(elv, elves, nswe, direction)
    p_.remove((x,y))
    if (x,y) not in p_:
      new_elfs[elf_id].r = x
      new_elfs[elf_id].c = y
      new_elfs[elf_id].d = (d+1) % 4
    else:
      new_elfs[elf_id].d = (d+1) % 4

  elves = new_elfs
  if time == 9:
    solution1 = calc_empty_space(new_elfs)

print(f'Solution1: {solution1}')
print(f'Solution2: {solution2}')
# pypy3 solution.py