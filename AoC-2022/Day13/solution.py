demo = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
import string
from functools import cmp_to_key

def parse_digit(L, R, x, y):
  i = int(L[x])
  j = int(R[y])
  if L[x+1] in string.digits:
    i = int(L[x:x+2])
    x+=1
  if R[y+1] in string.digits:
    j = int(R[y:y+2])
    y+=1
  x+=1
  y+=1
  return i,j,x,y


def check_order(L, R):
  x, y = 0, 0
  order_right = True
  i, j = 0, 0
  while x<len(L) and y<len(R):
    if L[x] in string.digits and R[y] in string.digits:
      i,j,x,y = parse_digit(L, R, x, y)

      if i > j:
        order_right = False
        break

      if i < j:
        order_right = True
        break

    if (L[x] in string.digits and R[y] == ']'):
      order_right = False
      break

    if (L[x] == ']' and R[y] in string.digits):
      order_right = True
      break

    if (L[x] == '[' and R[y] in string.digits):
      while L[x] == '[':
        x+=1
      if L[x] == ']':
        order_right = True
        break
      i,j,x,y = parse_digit(L, R, x, y)
      if i > j:
        order_right = False
        break
      if i < j:
        order_right = True
        break

    if (L[x] in string.digits and R[y] == '['):
      while R[y] == '[':
        y+=1
      if R[y] == ',':
        y+=1
        continue
      if R[y] == ']':
        order_right = False
        break
      i,j,x,y = parse_digit(L, R, x, y)
      if i > j:
        order_right = False
        break

      if i < j:
        order_right = True
        break

    if (L[x] == ','):
      x+=1

    if (R[y] == ','):
      y+=1

    if (L[x] == '[' and R[y] == '[') or (L[x] == ']' and R[y] == ']'):
      x+=1
      y+=1
      continue

    if L[x] == '[' and R[y] == ']':
      order_right = False
      break

    if L[x] == ']' and R[y] == '[':
      order_right = True
      break

  return order_right

inp = demo
inp = open('input.txt').read()
pairs = inp[:-1].split('\n\n')

correct_order = []
for idx, p in enumerate(pairs):
  L, R = p.split('\n')
  
  if check_order(L,R):
    correct_order.append(idx+1)
  
packet = inp[:-1].replace('\n\n', '\n').split('\n')
packet.append('[[2]]')
packet.append('[[6]]')

def cmp(x, y):
  if check_order(x, y):
    return -1
  else:
    return 1

sorted_packets = sorted(packet, key=cmp_to_key(cmp))

first = 0
second = 0
for idx, el in enumerate(sorted_packets):
  if el == '[[2]]':
    first = idx+1
  if el == '[[6]]':
    second = idx+1

print(f'Solution1: {sum(correct_order)}')
print(f'Solution2: {first*second}')

