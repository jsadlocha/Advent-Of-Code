def move(dir: str, s: list, count: int, visited: set):
  for j in range(count):
    if dir == 'R':
      s[0][0] += 1
    elif dir == 'L':
      s[0][0] -= 1
    elif dir == 'U':
      s[0][1] += 1
    elif dir == 'D':
      s[0][1] -= 1

    for i in range(1,len(s)):

      if abs(s[i-1][0] - s[i][0]) > 1 or abs(s[i-1][1] - s[i][1]) > 1:
        s[i][0] += 0 if (s[i-1][0] == s[i][0]) else 1 if (s[i-1][0] > s[i][0]) else -1
        s[i][1] += 0 if (s[i-1][1] == s[i][1]) else 1 if (s[i-1][1] > s[i][1]) else -1
        if i == (len(s)-1):
          visited.add((s[i][0],s[i][1]))

line = open('input.txt').read().split('\n')[:-1]
snake = [[0,0] for i in range(2)]
visited = set()
visited.add((0,0))

for i in line:
  op, count = i.split(' ')
  move(op, snake, int(count), visited)

snake = [[0,0] for i in range(10)]
visited2 = set()
visited2.add((0,0))
for i in line:
  op, count = i.split(' ')
  move(op, snake, int(count), visited2)

print(f'Solution1: {len(visited)}')
print(f'Solution2: {len(visited2)}')
