# with open('input.txt') as f:
#   sum = 0
#   while True:
#     if (len(el) > 0):
#       el = ord(el.pop())
#       if (el > 96 and el < 123):
#         sum += el - 96
#       if (el > 64 and el < 91):
#         sum += el - 38

with open('input.txt') as f:
  sum = 0
  while True:
    arr = []
    for i in range(3):
      arr.append(f.readline()[:-1])
    el = set(arr[0]) & set(arr[1]) & set(arr[2])
    if (len(el) > 0):
      el = ord(el.pop())
      if (el > 96 and el < 123):
        sum += el - 96
      if (el > 64 and el < 91):
        sum += el - 38
      print(sum)

 