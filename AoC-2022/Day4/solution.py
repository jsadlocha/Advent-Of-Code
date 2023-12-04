from functools import *

# sum = 0
# for epair in map(lambda x: x.split(','), open('input.txt').read().split('\n')[:-1]):
#   x, y = epair
#   x = x.split('-')
#   y = y.split('-')
#   if not(int(x[1]) < int(y[0]) or int(x[0]) > int(y[1])):
#     sum+=1
# print(sum)


# a = list(map(lambda x: x.split(','), open('input.txt').read().split('\n')[:-1]))
# b = list(map(lambda x: list(map(lambda x: x.split('-'), x)), a))
# c = map(lambda x: [1 if not(int(x[0][1])<int(x[1][0])or int(x[0][0])>int(x[1][1])) else 0], b)
# sum = reduce(lambda x, y: x+y, reduce(lambda x, y: x+y, c))
# print(sum)

# cmp1 = 
cmp2 = lambda x: [1 if not(int(x[0][1])<int(x[1][0])or int(x[0][0])>int(x[1][1])) else 0]

print(reduce(lambda x, y: x+y, reduce(lambda x, y: x+y, map(lambda x: [1 if not(int(x[0][1])<int(x[1][0])or int(x[0][0])>int(x[1][1])) else 0], map(lambda x: list(map(lambda x: x.split('-'), x)), map(lambda x: x.split(','), open('input.txt').read().split('\n')[:-1]))))))

# with open('input.txt', 'r') as f:
 