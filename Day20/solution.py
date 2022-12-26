demo = """1
2
-3
3
-2
0
4
"""

class Node:
  def __init__(self, x):
    self.x = x
    self.right = None
    self.left = None

inp = demo
inp = open('input.txt').read()
inp = inp.splitlines()

def mixin(nums):
  zero = None
  for n in nums:
    steps = n.x

    if steps == 0:
      zero = n
      continue

    if steps % (m-1) == 0:
      continue
    
    left = n.left
    right = n.right
    left.right = right
    right.left = left

    p = n
    if steps > 0:
      for j in range(steps % (m-1)):
        p = p.right

      l = p
      r = p.right
      l.right = n
      r.left = n
      n.left = l
      n.right = r

    else:
      for j in range(abs(steps) % (m-1)):
        p = p.left

      l = p.left
      r = p
      l.right = n
      r.left = n
      n.left = l
      n.right = r  
  return zero

nums = [Node(int(x)) for x in inp]
m = len(nums)
for i in range(m):
  nums[i].left = nums[(i-1) % m]
  nums[i].right = nums[(i+1) % m]

zero = mixin(nums)
total = 0
for j in range(1000, 3001, 1000):
  p_ = zero
  for i in range(j % (m)):
    p_ = p_.right
  total += p_.x



key = 811589153
nums = [Node(int(x)*key) for x in inp]
m = len(nums)
for i in range(m):
  nums[i].left = nums[(i-1) % m]
  nums[i].right = nums[(i+1) % m]

for i in range(10):
  zero = mixin(nums)

total2 = 0
for j in range(1000, 3001, 1000):
  p_ = zero
  for i in range(j % m):
    p_ = p_.right
  total2 += p_.x

print(f'Solution1: {total}')
print(f'Solution2: {total2}')
