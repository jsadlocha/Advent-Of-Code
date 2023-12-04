from collections import deque

def find_message(f, msg_len):
  deq = deque()
  for i in range(0,msg_len):
    deq.append(f[i])

  for i in range(msg_len, len(f)):
    if (len(set(deq)) == msg_len):
      print(i)
      break
    deq.popleft()
    deq.append(f[i])

file = open('input.txt').read()
find_message(file, 4)
find_message(file, 14)