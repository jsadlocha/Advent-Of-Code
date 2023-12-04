def check_clock():
  global clock
  global regx
  global sigsum

  if clock in [20, 60, 100, 140, 180, 220]:
    sigsum += clock * regx
    #print(f' {clock} {clock * regx} {regx}')

def crt():
  global clock
  global regx
  global screen

  col = (clock-1)//40
  row = (clock-1) % 40
  screen[col][row] = '#' if abs(row - regx) < 2 else '.'

line = open('input.txt').read().split('\n')[:-1]
clock = 1
regx = 1
sigsum = 0
screen = [[[] for j in range(40)] for i in range(6)]
for l in line:

  check_clock()
  crt()
  if l == "noop":
    clock += 1
    continue
  op, val = l.split(' ')

  if op == "addx":
    clock += 1
    check_clock()
    crt()
    regx += int(val)
    clock += 1
    continue

print(f'Solution1: {sigsum}')

print(f'Solution2:')
for line in screen:
  print(''.join(line))