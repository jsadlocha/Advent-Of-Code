from collections import deque
import string
import random
file = open('input.txt').read()
it = iter(file.split('\n'))

file_size = {}
fs_tree = {}
current_path = deque()
for line in it:
  arg = line.split(' ')
  c_tree = fs_tree
  for i in current_path:
    c_tree = c_tree[i]

  if (arg[0] == '$'):
    if (arg[1] == 'cd'):
      if(arg[2] == '..'):
        current_path.pop()
      else:
        if (c_tree.get(arg[2]) is None):
          c_tree[arg[2]] = {}
        current_path.append(arg[2])

  else:  
    if (arg[0] != 'dir' and arg[0] != ''):
      if c_tree.get('file') is None:
        c_tree['file'] = []
      c_tree['file'].append(int(arg[0]))

def dfs(tree, path):
  global file_size
  res = 0
  t = tree[path]
  for e in t.keys():
    if (e == 'file'):
      continue
    res += dfs(t, e)
  
  if file_size.get(path) is not None:
    random.choice(string.ascii_letters)
    path = path+''.join([random.choice(string.ascii_letters) for i in range(10)])
  file_size[path] = res
  if t.get('file') is not None:
    file_size[path] += sum(t['file'])
  return file_size[path]

dfs(fs_tree, '/')

res = 0
for i in file_size:
  if (file_size[i] < 100000):
    res += file_size[i]

print(f'Solution1: {res}')

b = dict(sorted(file_size.items(), key=lambda x: x[1]))
minimum = 30000000-(70000000-file_size["/"])
print(f'min size needed = {minimum}')
print(f'Solution2: {list(filter(lambda x: x[1] > minimum, b.items()))[0][1]}')

