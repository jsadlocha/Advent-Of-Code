from dataclasses import dataclass

@dataclass
class Point:
  x: int
  y: int

@dataclass
class Snake:
  head: Point
  tail: Point

def move(dir: str, s: Snake, count: int, visited: set):
  for i in range(count):
    x, y = s.head.x, s.head.y
    if dir == 'R':
      s.head.x += 1
    elif dir == 'L':
      s.head.x -= 1
    elif dir == 'U':
      s.head.y += 1
    elif dir == 'D':
      s.head.y -= 1

    if abs(s.head.x - s.tail.x) > 1 or abs(s.head.y - s.tail.y) > 1:
      s.tail.x = x
      s.tail.y = y
      visited.add((x,y))


  
line = open('input.txt').read().split('\n')
snake = Snake(Point(0,0), Point(0,0))
visited = set()
visited.add((0,0))
for i in line[:-1]:
  op, count = i.split(' ')

  move(op, snake, int(count), visited)


print(f'Solution1: {len(visited)}')
