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
# inp = demo
inp = open('input.txt').read()
inp = inp.splitlines()

arr = []
for line in inp:
  x,y,z = map(int, line.split(','))
  count_side = 6
  for l in inp:
    x2, y2, z2 = map(int, l.split(','))
    if (x,y,z) == (x2,y2,z2):
      continue
    if abs(x-x2) < 2 and y==y2 and z==z2:
      count_side -= 1
      
    if x==x2 and abs(y-y2) < 2 and z==z2:
      count_side -= 1
      
    if x==x2 and y==y2 and abs(z-z2) < 2:
      count_side -= 1
      
  arr.append((x,y,z, count_side))

sum = 0
for i in arr: 
  sum+=i[3]


print(f'Solution1: {sum}')
# print(f'Solution2: {sum2}')