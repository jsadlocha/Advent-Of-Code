demo = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
inp = demo
inp = open('input.txt').read()
inp = inp.splitlines()

from collections import deque
from functools import lru_cache

# right, back, up, left, front, down
offset1 = [(0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5), (-0.5, 0, 0), (0, -0.5, 0), (0, 0, -0.5)]
offset = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
faces = {}
cubes = set()
for line in inp:
  x, y, z = map(int, line.split(','))
  cubes.add((x,y,z))
  for dx, dy, dz in offset1:
    f = (x+dx, y+dy, z+dz)
    if f not in faces:
      faces[f] = 0
    faces[f] += 1

sum1 = list(faces.values()).count(1)

xs = [x for x,y,z in cubes]
minx, maxx = min(xs), max(xs)
ys = [y for x,y,z in cubes]
miny, maxy = min(ys), max(ys)
zs = [z for x,y,z in cubes]
minz, maxz = min(zs), max(zs)

@lru_cache(None)
def can_get_out(x, y, z):
  queue = deque()
  queue.append((x,y,z))
  visited = set()

  while queue:
    x, y, z = queue.popleft()
    if (x, y, z) in visited:
      continue
    visited.add((x,y,z))
    if (x, y, z) in cubes:
      continue
    
    if (x>=maxx or x<=minx or y>=maxy or y<=miny or 
        z>=maxz or z<=minz):
      return True

    for dx, dy, dz in offset:
      queue.append((x+dx, y+dy, z+dz))
  
  return False

sum2 = 0
for x,y,z in cubes:
  for dx, dy, dz in offset:
    if can_get_out(x+dx, y+dy, z+dz):
      sum2 += 1

print(f'Solution1: {sum1}')
print(f'Solution2: {sum2}')
