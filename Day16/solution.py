
demo = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

import re
from collections import deque
import time
inp = demo
inp = open('input.txt').read() 
inp = inp.splitlines()

valve_dict = {}
pattern_valve = r'[A-Z]{2}'
pattern_digit = r'\d+'

# parse input
for line in inp:
  valve = re.findall(pattern_valve, line)
  rate = re.findall(pattern_digit, line)
  valve_dict[valve[0]] = [int(rate[0]), valve[1:]]

sum = 0
for i in valve_dict:
  sum += valve_dict[i][0]

non_zero_valve = []
for edge in valve_dict:
  if valve_dict[edge][0] != 0:
    non_zero_valve.append(edge)

all_valve = ['AA'] + non_zero_valve[:]
valve_dist_path = {}
# BFS
for edge in all_valve:
  valve_list = valve_dict[edge][1]
  queue = deque()
  to_visit = len(all_valve)-1
  visited = {}
  dist_list = {}
  for el in valve_list:
    queue.append((el, 1))
  
  while queue:
    valve, dist = queue.popleft()
    if valve == edge or valve in visited:
      continue

    visited[valve] = True
    if valve in non_zero_valve:
      dist_list[valve] = dist

    for el in valve_dict[valve][1]:
      queue.append((el, dist+1)) 
    
  valve_dist_path[edge] = dist_list
  
sum_bits = 0
indices = {}
for idx, edge in enumerate(non_zero_valve):
  indices[edge] = idx
  sum_bits |= (1<<idx)

cache = {}
def DFS(edge, remaining_time, valve_bit, sum_counted):
  if remaining_time < 1:
    return sum_counted

  if (edge, remaining_time, valve_bit) in cache:
    return cache[(edge, remaining_time, valve_bit)]

  max_val = sum_counted
  for v, d in valve_dist_path[edge].items():
    if valve_bit & (1 <<indices[v]):
      continue
    r = remaining_time
    r -= d

    bit = valve_bit | (1 << indices[v])
    s = sum_counted + valve_dict[v][0]*(r-1)
    ret = DFS(v, r-1, bit, s)
    max_val = max(max_val, ret)
  
  cache[(edge, remaining_time-1, valve_bit)] = max_val
  return max_val

print(f'Solution 1: {DFS("AA", 30, 0, 0)}')

cache = {}
max_v = 0
for i in range(sum_bits//2):
  human = i
  elphant = sum_bits-i
  cache = {}
  max_v = max(max_v, DFS('AA', 26, human, 0)+DFS('AA', 26, elphant, 0))

print(f'Solution2: {max_v}')