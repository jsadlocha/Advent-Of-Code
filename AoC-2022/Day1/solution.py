arr = []
with open('input.txt') as f:
  sum = 0
  while True:
    line = f.readline()
    if(len(line) < 1):
      break

    if (len(line) == 1):
      arr.append(sum)
      sum = 0
      continue
    sum += int(line)

arr.sort(reverse=True)
print(f'Solution1: {arr[0]}')
print(f'Solution2: {arr[0]+arr[1]+arr[2]}')