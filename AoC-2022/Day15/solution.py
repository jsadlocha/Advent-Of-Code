import re

def manhatan_distance(p1, p2):
  return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def search_row(sensor_beacon, find_row):
  occupaied = set()
  for sens, beac in sensor_beacon:
    dist = manhatan_distance(sens, beac)
    requir_dist = abs(find_row - sens[1])
    if requir_dist < dist:
      left_dist = dist - requir_dist
      low_col  = sens[0] + left_dist
      high_col = sens[0] - left_dist
      if low_col > high_col:
        low_col, high_col = high_col, low_col
      for col in range(low_col, high_col+1):
        occupaied.add((find_row, col))
  return occupaied

inp = open('input.txt').read()
inp = [list(map(int, re.findall(r'-?\d+', x))) for x in inp.splitlines()]

sensor_beacon = []
for line in inp:
  x, y, x2, y2 = line
  sensor_beacon.append(((x,y),(x2,y2)))

def find_empty_space(max_rows):
  for row in range(max_rows+1):
    intervals = []
    for line in inp:
      x, y, x2, y2 = line

      d = abs(x-x2)+abs(y-y2)
      r_dist = d - abs(y-row)
      if r_dist < 0:
        continue

      lo = x-r_dist
      hi = x+r_dist
      intervals.append((lo, hi))

    intervals.sort()
    idx = 0
    for lo, hi in intervals:
      if idx >= lo and idx <= hi:
        idx = hi
        idx+=1

    if idx <= 4000000:
      return (row, idx)

max_rows = 4000000
row, col = find_empty_space(max_rows)
print(f'Solution1: {len(search_row(sensor_beacon, 2000000))-1}')
print(f'Solution2: {col*max_rows+row}')



